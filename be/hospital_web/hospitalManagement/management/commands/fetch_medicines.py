from django.core.management.base import BaseCommand
import requests
from hospitalManagement.models import Medicine

class Command(BaseCommand):
    help = 'Fetches up to 10 valid medicine entries from OpenFDA API and stores them in the database'

    def handle(self, *args, **kwargs):
        total_to_save = 10
        saved_count = 0
        offset = 0
        seen_offsets = 0
        max_attempts = 10  # avoid infinite loop

        self.stdout.write("Fetching valid medicine entries from OpenFDA...")

        while saved_count < total_to_save and seen_offsets < max_attempts:
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

                # Prefer a clean, purpose-driven field
                usage = item.get("indications_and_usage", [None])[0]
                fallback_description = item.get("description", [None])[0]
                raw_description = usage or fallback_description

                # Skip invalid entries
                if not generic_name or not brand_name or not manufacturer or not raw_description:
                    continue

                # Format name and truncate description
                combined_name = f"{brand_name} ({generic_name})"
                description_words = raw_description.split()
                short_description = ' '.join(description_words[:100])
                if len(description_words) > 100:
                    short_description += '...'

                try:
                    medicine, created = Medicine.objects.get_or_create(
                        name=combined_name,
                        brand=manufacturer,
                        defaults={
                            'description': short_description,
                            'times_per_day': 0,
                            'price': 0.00
                        }
                    )
                    if created:
                        saved_count += 1
                        self.stdout.write(self.style.SUCCESS(f"[{saved_count}/{total_to_save}] Saved: {medicine.name}"))
                        if saved_count >= total_to_save:
                            break
                except Exception as e:
                    self.stderr.write(f"Error saving medicine: {e}")
                    continue

            offset += 10
            seen_offsets += 1

        self.stdout.write(self.style.SUCCESS(f"Done. {saved_count} medicine entries saved."))
        if saved_count < total_to_save:
            self.stdout.write(self.style.WARNING("Could not find enough valid entries."))
