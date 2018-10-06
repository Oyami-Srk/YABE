source active
echo "Successfully active VENV"
python3 -m yabe drop_all_database
echo "Dropped!"
python3 -m yabe create_all_database
echo "Created!"
python3 -m yabe fill_test_data
echo "Filled!"
