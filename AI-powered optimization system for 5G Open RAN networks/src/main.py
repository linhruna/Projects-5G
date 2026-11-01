import argparse
from datetime import datetime

from src.config import LOGS_DIR, PREDICTIONS_DIR
from src.utils.logger import get_logger
from src.data_preparation.data_extraction import extract_data
from src.data_preparation.data_cleaning import clean_data
from src.data_preparation.data_transformation import transform_data
from src.models.predictive_network_planning.predict import make_predictions

def main(args):
    # Set up logger
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    log_name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
    logger = get_logger(__name__, log_file=log_name)
    
    # Extract data
    logger.info("Extracting data...")
    raw_data = extract_data(args.data_file)
    
    # Clean data
    logger.info("Cleaning data...")
    cleaned = clean_data(raw_data)
    
    # Transform data
    logger.info("Transforming data...")
    transformed_data = transform_data(cleaned)
    
    # Make predictions
    logger.info("Making predictions...")
    predictions = make_predictions(transformed_data)
    
    # Save predictions to file
    logger.info("Saving predictions to file...")
    predictions_file = PREDICTIONS_DIR / f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    predictions.to_csv(predictions_file, index=False)
    
    logger.info(f"Finished. Wrote: {predictions_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main program.")
    parser.add_argument("data_file", type=str, help="Path to the raw data file.")
    args = parser.parse_args()
    
    main(args)

