import indiapins
import json

def fetch_new_delhi_zipcodes():
    new_delhi_zipcodes = set()
    for zipcode in range(110000, 120000):
        try:
            pin_details = indiapins.matching(str(zipcode))
            for detail in pin_details:
                if detail['State'] == 'Delhi':
                    new_delhi_zipcodes.add(detail['Pincode'])
        except Exception as e:
            continue
    return list(new_delhi_zipcodes)

if __name__ == "__main__":
    new_delhi_zipcodes = fetch_new_delhi_zipcodes()
    with open('new_delhi_zipcodes.json', 'w') as f:
        json.dump(new_delhi_zipcodes, f)
    print(f"Fetched and stored {len(new_delhi_zipcodes)} New Delhi zip codes.")
