#!/bin/bash

usage() {
  echo "Usage: $0 [-s|--schema SCHEMA] [-p|--password PASSWORD]" >&2
  echo "Example: $0 -s my_schema -p my_password" >&2
  exit 1
}

extract_arguments() {
  while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      -s|--schema)
        SCHEMA="$2"
        shift
        shift
        ;;
      --schema=*)
        SCHEMA="${key#*=}"
        shift
        ;;
      -p|--password)
        PASSWORD="$2"
        shift
        shift
        ;;
      --password=*)
        PASSWORD="${key#*=}"
        shift
        ;;
      *)
        echo "Unknown option: $key" >&2
        usage
        ;;
    esac
  done
}


usage_analyst() {
  echo "Usage: $0 [-s|--schema SCHEMA] [-p|--password PASSWORD] [-t|--table TABLE]" >&2
  echo "Example: $0 -s my_schema -p my_password --table=users" >&2
  exit 1
}

extract_arguments_analyst() {
  while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      -s|--schema)
        SCHEMA="$2"
        shift
        shift
        ;;
      --schema=*)
        SCHEMA="${key#*=}"
        shift
        ;;
      -p|--password)
        PASSWORD="$2"
        shift
        shift
        ;;
      --password=*)
        PASSWORD="${key#*=}"
        shift
        ;;
      -t|--table)
        TABLE="$2"
        shift
        shift
        ;;
      --table=*)
        TABLE="${key#*=}"
        shift
        ;;
      *)
        echo "Unknown option: $key" >&2
        usage_analyst
        ;;
    esac
  done
}