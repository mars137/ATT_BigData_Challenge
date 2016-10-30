from setuptools import setup

setup(name='sentiment_analyzer',
      version='2.0',
      description='Sentiment Analyzer for twitter feed, yelp and google reviews to compare with A&T retail store performance',
      url='http://github.com/mars137/Data_Challenge',
      author='Atif Tahir',
      author_email='atif.tahir@etamu.edu',
      license='MIT',
      install_requires=['requests','oauth2','nose','coverage','textblob','nltk', 'progressbar'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
