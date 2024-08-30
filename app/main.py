import yaml
import psycopg2
import csv

def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def export_data_to_csv(config):
    conn = psycopg2.connect(
        dbname=config['connections']['database1']['url'],
        user=config['connections']['database1']['login'],
        password=config['connections']['database1']['password']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")  # Replace with your SQL query
    rows = cursor.fetchall()
    
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    cursor.close()
    conn.close()

def import_data_from_csv(config):
    conn = psycopg2.connect(
        dbname=config['connections']['database2']['url'],
        user=config['connections']['database2']['login'],
        password=config['connections']['database2']['password']
    )
    cursor = conn.cursor()
    
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cursor.execute("INSERT INTO your_table VALUES (%s, %s, %s)", row)  # Adjust based on your table structure
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    config = read_config('app/config.yaml')
    export_data_to_csv(config)
    import_data_from_csv(config)
