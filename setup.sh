
export DATABASE_URL='postgresql://postgres:091297@localhost:5432/casting'
export AUTH0_DOMAIN='aschonn.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='casting'


#DATABASE_URL should be set in setup.sh and pass it to models.py using database_path = os.environ['DATABASE_URL]
#As in Heruoku you will set the DATABASE_URL to the postgressql addon you created on Heroku.
#in you setup.sh you could set DATABASE_URL to you local database url, but on heroku it is supposed to be the DATABASE_URL you created on heroku

#DATABASE_URL: postgres://vgaidjkhnksymk:8866d2ae6408947eb238d724326b43d7f217d072461e5b9f399c997e07e9d274@ec2-52-202-146-43.compute-1.amazonaws.com:5432/d4h14pmc2hrp8f
#https://aschonn.us.auth0.com/authorize?audience=casting&response_type=token&client_id=ZNgxU9gxuFqVJmp5zK7cr2Dc6HL4nt0p&redirect_uri=http://127.0.0.1:8080