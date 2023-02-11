# Turplanlegger
Python API for planning trips

## Install
```bash
pip install .
```

### Development
```bash
pip install .[dev]
```

## Testing
Run test:
```
pip install pytest
pytest tests/test_*.py`
```

Run test and save result:
```
pip install pytest pytest-csv
pytest tests/test_*.py --csv tests/test_result.csv --csv-columns utc_timestamp,id,module,name,file,status,message,duration
git commit tests/test_result.csv -m "Unitetest result"
```


## Docker

### Test
`docker-compose -f docker-compose.test.yml up --abort-on-container-exit  --exit-code-from turplanlegger-api`

### Dev
`docker-compose -f docker-compose.dev.yml up --abort-on-container-exit  --exit-code-from turplanlegger-api`

### Prod
`docker-compose up --abort-on-container-exit  --exit-code-from turplanlegger-api`