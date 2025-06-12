from django.core.management.base import BaseCommand
import requests
import time
from hospitalManagement.models import Medicine
from hospitalManagement.utils.gemini_client import process_medicine_description_with_gemini

class Command(BaseCommand):
    help = 'Fetches medicine entries from OpenFDA, processes descriptions with Gemini, and saves to DB'

    def handle(self, *args, **kwargs):
        saved_count = 0
        gemini_calls = 0
        offset = 0
        limit = 100
        gemini_quota=15;
        self.stdout.write("Fetching valid medicine entries from OpenFDA...")
        try:
            while True:
                url = f"https://api.fda.gov/drug/label.json?limit={limit}&skip={offset}"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json().get("results", [])
                except requests.RequestException as e:
                    self.stderr.write(f"API request failed: {e}")
                    return

                if not data:
                    self.stdout.write("No more data received from OpenFDA.")
                    break

                for item in data:
                    # Extract fields
                    generic_name = item.get("openfda", {}).get("generic_name", [None])[0]
                    brand_name = item.get("openfda", {}).get("brand_name", [None])[0]
                    manufacturer = item.get("openfda", {}).get("manufacturer_name", [None])[0]
                    usage = item.get("indications_and_usage", [None])[0]
                    description = item.get("description", [None])[0]

                    if not all([generic_name, brand_name, manufacturer, usage, description]):
                        continue

                    combined_name = f"{brand_name} ({generic_name})".strip().title()
                    manufacturer = manufacturer.strip().title()

                    # Skip existing
                    if Medicine.objects.filter(name=combined_name, brand=manufacturer).exists():
                        self.stdout.write(f"Skipped existing medicine: {combined_name}")
                        continue

                    try:
                        ai_result = process_medicine_description_with_gemini(usage, description)
                        gemini_calls += 1

                        translated_summary = ai_result.get("translated_summary", "")
                        times_per_day = ai_result.get("times_per_day", 0)
                        estimated_price = ai_result.get("estimated_price", 0.0)

                        Medicine.objects.create(
                            name=combined_name,
                            brand=manufacturer,
                            description=translated_summary,
                            times_per_day=times_per_day,
                            price=estimated_price
                        )

                        saved_count += 1
                        self.stdout.write(self.style.SUCCESS(f"[{saved_count}] Saved: {combined_name}"))

                        # Pause after reaching Gemini quota
                        if gemini_calls >= gemini_quota:
                            self.stdout.write("Reached maximum Gemini calls per minute. Waiting 65 seconds to refresh quota...")
                            time.sleep(65)
                            gemini_calls = 0

                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Processing failed for '{combined_name}': {e}. Stopping command to preserve quota."))
                        return

                # Move to next batch
                offset += limit
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nCommand interrupted by user."))
        finally:
            self.stdout.write(self.style.SUCCESS(f"Total medicine entries saved before exit: {saved_count}"))
