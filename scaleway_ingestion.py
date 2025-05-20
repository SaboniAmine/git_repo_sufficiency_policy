#!/usr/bin/env python3

"""
Scaleway Abstract Ingestion Script

This script extracts policies, outcomes and correlations from academic abstracts using Scaleway's OpenAI API.
It processes a Parquet file containing abstracts and outputs a list of Pydantic objects with extracted features.

Usage:
    python scaleway_ingestion.py --input <input_parquet_path> --output <output_json_path>

Required arguments:
    --input: Path to the input Parquet file containing abstracts
    --output: Path where the JSON file with extracted features will be saved
"""

import argparse
import os
import json
import time
from typing import Optional, List, Dict, Tuple
from datetime import datetime
from multiprocessing import Pool, cpu_count

import pandas as pd
from openai import OpenAI
from persist_policies import persist_policies
from prompts import generate_abstract_analysis_prompt


def init_client():
    """Initialize the OpenAI client for each worker process."""
    global client
    scaleway_api_key = os.getenv('SCW_SECRET_KEY', "") # Amine
    client = OpenAI(
        base_url="https://api.scaleway.ai/94312233-a90c-43bf-adfc-a72437bdfb3c/v1",
        api_key=scaleway_api_key
    )


def extract_features_and_correlations(text: str) -> Tuple[Optional[str], Dict]:
    """
    Extract features and correlations from an abstract using Scaleway's OpenAI API.
    
    Args:
        text: The abstract text to analyze
        
    Returns:
        Tuple of (extracted data or None if processing failed, metrics dictionary)
    """
    if not text.strip():
        return None, {"tokens": 0, "time": 0}

    # Generate the prompt using the template
    prompt = generate_abstract_analysis_prompt(text)
    
    # Define the JSON schema for the response
    json_schema = {
        "type": "object",
        "properties": {
            "GEOGRAPHIC": {"type": "string"},
            "items": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "FACTOR": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "object",
                                "properties": {
                                    "CORRELATION": {"type": "string"}
                                },
                                "required": ["CORRELATION"]
                            }
                        }
                    },
                    "required": ["FACTOR"]
                }
            }
        },
        "required": ["GEOGRAPHIC", "items"]
    }
    
    start_time = time.time()
    try:
        print(f"Processing abstract: {text}...")
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "schema": json_schema,
                    "name": "output_schema",
                    "strict": True
                }
            }
        )
        
        # Calculate metrics
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Get token usage
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        metrics = {
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": total_tokens
            },
            "time": processing_time
        }
        
        extracted_data = json.loads(response.choices[0].message.content.strip())
        persisted_data = persist_policies(extracted_data, text)
        extracted_data.update({"abstract": text})
        print(f"Extracted data: {extracted_data}")
        print(f"Metrics: {metrics}")
        return extracted_data, metrics
        
    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"Error processing abstract: {e}")
        return None, {"tokens": 0, "time": processing_time}


def process_abstracts(abstracts: List[str]) -> List[Tuple[Optional[str], Dict]]:
    """
    Process a list of abstracts using multiprocessing.
    
    Args:
        abstracts: List of abstract texts to process
        
    Returns:
        List of tuples containing (extracted data, metrics)
    """
    with Pool(processes=4, initializer=init_client) as pool:
        results = pool.map(extract_features_and_correlations, abstracts)
    return results


def main():
    parser = argparse.ArgumentParser(description='Process abstracts to extract features and correlations.')
    parser.add_argument('--input', required=True, help='Path to input Parquet file containing abstracts')
    parser.add_argument('--output', required=True, help='Path to save the JSON file with extracted features')
    
    args = parser.parse_args()
    
    # Read input data
    print(f"Reading input data from {args.input}")
    df = pd.read_parquet(args.input)
    df["abstract"] = df["abstract"].fillna("").astype(str)
    
    # Start timing the entire process
    total_start_time = time.time()
    
    # Process abstracts using multiprocessing
    print(f"Processing {len(df)} abstracts using 4 workers")
    results_with_metrics = process_abstracts(df['abstract'].tolist())
    
    # Calculate total processing time
    total_time = time.time() - total_start_time
    
    # Separate results and metrics
    results = []
    metrics_list = []
    total_tokens = 0
    
    for result, metrics in results_with_metrics:
        if result is not None:
            results.append(result)
            metrics_list.append(metrics)
            total_tokens += metrics["tokens"]["total"]
    
    # Calculate and print summary statistics
    print("\nSummary Statistics:")
    print(f"Total abstracts processed: {len(results)}")
    print(f"Total tokens used: {total_tokens}")
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Average tokens per request: {total_tokens/len(results) if results else 0:.2f}")
    print(f"Average time per request: {total_time/len(results) if results else 0:.2f} seconds")
    
    # Save results
    print(f"\nSaving results to {args.output}")
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print("Processing complete!")


if __name__ == "__main__":
    main() 