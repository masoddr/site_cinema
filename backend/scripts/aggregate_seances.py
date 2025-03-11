from app.scrapers.aggregator import SeanceAggregator

def main():
    aggregator = SeanceAggregator()
    aggregator.save_to_json('all_seances.json')
    print("Toutes les séances ont été agrégées dans all_seances.json")

if __name__ == "__main__":
    main() 