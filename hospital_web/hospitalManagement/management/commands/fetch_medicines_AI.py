from django.core.management.base import BaseCommand
import requests
from hospitalManagement.models import Medicine
from hospitalManagement.utils.gemini_client import process_medicine_description_with_gemini

class Command(BaseCommand):
    help = 'Fetches medicine entries from OpenFDA, processes descriptions with Gemini, and saves to DB'

    def handle(self, *args, **kwargs):
        total_to_save = 10
        saved_count = 0
        offset = 0
        max_attempts = 10

        self.stdout.write("Fetching valid medicine entries from OpenFDA...")

        while saved_count < total_to_save and offset < max_attempts * 10:
            url = f"https://api.fda.gov/drug/label.json?limit=10&skip={offset}"
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
                generic_name = item.get("openfda", {}).get("generic_name", [None])[0]
                brand_name = item.get("openfda", {}).get("brand_name", [None])[0]
                manufacturer = item.get("openfda", {}).get("manufacturer_name", [None])[0]

                usage = item.get("indications_and_usage", [None])[0]
                fallback_description = item.get("description", [None])[0]
                raw_description = usage or fallback_description

                if not all([generic_name, brand_name, manufacturer, raw_description]):
                    continue

                combined_name = f"{brand_name} ({generic_name})"

                try:
                    ai_result = process_medicine_description_with_gemini(raw_description)
                    translated_summary = ai_result.get("translated_summary", "")
                    times_per_day = ai_result.get("times_per_day", 0)
                    estimated_price = ai_result.get("estimated_price", 0.0)

                    medicine, created = Medicine.objects.get_or_create(
                        name=combined_name,
                        brand=manufacturer,
                        defaults={
                            'description': translated_summary,
                            'times_per_day': times_per_day,
                            'price': estimated_price
                        }
                    )

                    if created:
                        saved_count += 1
                        self.stdout.write(self.style.SUCCESS(f"[{saved_count}/{total_to_save}] Saved: {medicine.name}"))
                        if saved_count >= total_to_save:
                            return

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Processing failed for '{combined_name}': {e}. Stopping command to preserve quota."))
                    return

            offset += 10

        self.stdout.write(self.style.SUCCESS(f"Done. {saved_count} medicine entries saved."))
        if saved_count < total_to_save:
            self.stdout.write(self.style.WARNING("Could not find enough valid entries."))