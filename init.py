"""
Add a layer between our database and application through the use of an Object Relational Mapper.
This lets us map our Python objects with our SQL database.
"""

# Installed import packages
from flask_sqlalchemy import SQLAlchemy

# Initialise by creating a single instance of the Object Relational Mapper that we can refer to throughout the code
db = SQLAlchemy()