"""
Parser module for ZMap SDK
"""

import csv
import json
import os
from collections.abc import Iterator
from typing import Any

from zmapsdk.exceptions import ZMapParserError


class ZMapParser:
    """
    Class for parsing ZMap output files
    """

    @staticmethod
    def parse_csv_results(
        file_path: str,
        fields: list[str] | None = None,
    ) -> list[dict[str, str]]:
        """
        Parse a CSV results file from ZMap

        Args:
            file_path: Path to the CSV file
            fields: List of field names (if not provided, will try to read from header)

        Returns:
            List of dictionaries, each representing a row with field names as keys

        Raises:
            ZMapParserError: If the file can't be parsed
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Results file not found: {file_path}")

        try:
            results = []
            with open(file_path) as f:
                # Check if file has a header
                first_line = f.readline().strip()
                f.seek(0)  # Reset to beginning of file

                # If fields not provided and first line contains commas, try to use it as header
                if fields is None and "," in first_line:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results.append(dict(row))
                # If fields provided, use them as column names
                elif fields:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) != len(fields):
                            raise ZMapParserError(
                                f"CSV row has {len(row)} fields, but {len(fields)} field names provided",
                            )
                        results.append(
                            {field: value for field, value in zip(fields, row)},
                        )
                # If only IPs (single column), treat each line as an IP
                else:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) == 1:
                            results.append({"saddr": row[0]})
                        else:
                            raise ZMapParserError(
                                "CSV has multiple columns but no field names provided",
                            )

            return results

        except (csv.Error, OSError) as e:
            raise ZMapParserError(f"Failed to parse CSV results: {e!s}")

    @staticmethod
    def parse_json_results(file_path: str) -> list[dict[str, Any]]:
        """
        Parse a JSON results file from ZMap

        Args:
            file_path: Path to the JSON file

        Returns:
            List of dictionaries from the JSON file

        Raises:
            ZMapParserError: If the file can't be parsed
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Results file not found: {file_path}")

        try:
            with open(file_path) as f:
                data = json.load(f)

            # Handle both array and object formats
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ZMapParserError(f"Unexpected JSON format: {type(data)}")

        except (json.JSONDecodeError, OSError) as e:
            raise ZMapParserError(f"Failed to parse JSON results: {e!s}")

    @staticmethod
    def parse_metadata(file_path: str) -> dict[str, Any]:
        """
        Parse a ZMap metadata file (JSON format)

        Args:
            file_path: Path to the metadata file

        Returns:
            Dictionary containing metadata

        Raises:
            ZMapParserError: If the file can't be parsed
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Metadata file not found: {file_path}")

        try:
            with open(file_path) as f:
                return json.load(f)

        except (json.JSONDecodeError, OSError) as e:
            raise ZMapParserError(f"Failed to parse metadata: {e!s}")

    @staticmethod
    def parse_status_updates(file_path: str) -> list[dict[str, Any]]:
        """
        Parse a ZMap status updates file (CSV format)

        Args:
            file_path: Path to the status updates file

        Returns:
            List of dictionaries, each representing a status update

        Raises:
            ZMapParserError: If the file can't be parsed
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Status updates file not found: {file_path}")

        try:
            updates = []
            with open(file_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert numeric fields to appropriate types
                    for key, value in row.items():
                        if key in ["time", "sent", "recv", "hits", "cooldown_secs"]:
                            try:
                                row[key] = float(value) if "." in value else int(value)
                            except ValueError:
                                pass  # Keep as string if conversion fails
                    updates.append(row)

            return updates

        except (csv.Error, OSError) as e:
            raise ZMapParserError(f"Failed to parse status updates: {e!s}")

    @staticmethod
    def extract_ips(
        results: list[dict[str, Any]],
        ip_field: str = "saddr",
    ) -> list[str]:
        """
        Extract IP addresses from parsed results

        Args:
            results: List of result dictionaries
            ip_field: Field name containing IP addresses

        Returns:
            List of IP addresses

        Raises:
            ZMapParserError: If the IP field is missing from any result
        """
        try:
            return [result[ip_field] for result in results]
        except KeyError:
            raise ZMapParserError(f"IP field '{ip_field}' not found in results")

    @staticmethod
    def stream_results(
        file_path: str,
        fields: list[str] | None = None,
    ) -> Iterator[dict[str, str]]:
        """
        Stream results from a CSV file without loading everything into memory

        Args:
            file_path: Path to the CSV file
            fields: List of field names (if not provided, will try to read from header)

        Yields:
            Dictionaries, each representing a row with field names as keys

        Raises:
            ZMapParserError: If the file can't be parsed
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Results file not found: {file_path}")

        try:
            with open(file_path) as f:
                # Check if file has a header
                first_line = f.readline().strip()
                f.seek(0)  # Reset to beginning of file

                # If fields not provided and first line contains commas, try to use it as header
                if fields is None and "," in first_line:
                    reader = csv.DictReader(f)
                    for row in reader:
                        yield dict(row)
                # If fields provided, use them as column names
                elif fields:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) != len(fields):
                            raise ZMapParserError(
                                f"CSV row has {len(row)} fields, but {len(fields)} field names provided",
                            )
                        yield {field: value for field, value in zip(fields, row)}
                # If only IPs (single column), treat each line as an IP
                else:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) == 1:
                            yield {"saddr": row[0]}
                        else:
                            raise ZMapParserError(
                                "CSV has multiple columns but no field names provided",
                            )

        except (csv.Error, OSError) as e:
            raise ZMapParserError(f"Failed to parse CSV results: {e!s}")

    @staticmethod
    def count_results(file_path: str) -> int:
        """
        Count the number of results in a file without loading everything into memory

        Args:
            file_path: Path to the results file

        Returns:
            Number of result rows

        Raises:
            ZMapParserError: If the file can't be read
        """
        if not os.path.isfile(file_path):
            raise ZMapParserError(f"Results file not found: {file_path}")

        try:
            with open(file_path) as f:
                # Check if it's a CSV with header
                first_line = f.readline().strip()
                has_header = "," in first_line

                # Start count at 0 if header, 1 if already counted first row
                count = 0 if has_header else 1

                # Count remaining lines
                for _ in f:
                    count += 1

            return count

        except OSError as e:
            raise ZMapParserError(f"Failed to read results file: {e!s}")
