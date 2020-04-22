import http.client

class countrywise:
    def send_country_info(self):
        conn = http.client.HTTPSConnection("coronavirus-tracker-india-covid-19.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "coronavirus-tracker-india-covid-19.p.rapidapi.com",
            'x-rapidapi-key': "f5cf3d138fmsh6da1c6d23ddd179p1d4340jsn31ed04478fab"
            }

        conn.request("GET", "/api/getStatewise", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return(data.decode("utf-8"))