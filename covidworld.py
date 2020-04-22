import http.client
#worldwide statistics

class worldwide:
    def send_world_info(self):
        conn = http.client.HTTPSConnection("covid-19-statistics.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
            'x-rapidapi-key': "f5cf3d138fmsh6da1c6d23ddd179p1d4340jsn31ed04478fab"
            }

        conn.request("GET", "/reports/total?date=2020-04-07", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return(data.decode("utf-8"))
