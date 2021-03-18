import unittest
import requests_mock
import requests
import json


class TestFunction(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_add_event(self):
        payload = json.dumps({
                  "contact_name": "chinni",
                  "contact_phone_number": "7893877745",
                  "description": "Description",
                  "notes": "notes !!",
                  "status": "Complete"
        })
        response = requests.post("http://localhost:5000/api/v1/events",headers={"Content-Type": "application/json"}, data=payload)
        response_body =response.json()
        # print("response {}".format(response_body))
        content=response_body["response"]
        status= response_body["status"]
        # print(status)
        assert status=='201'
        assert content["contact_name"] =="chinni"


    def test_get_events(self):
        response = requests.get("http://localhost:5000/api/v1/events")
        response_body =response.json()
        # print("response {} \n length {}".format(response_body,len(response_body)))
        last_object=response_body[-1]
        # print("last_object  ",last_object)
        assert response.status_code == 200
        assert len(response_body) ==last_object['id']

    def test_update_course(self):
        payload = json.dumps({
              "notes": "notes !!",
              "status": "Complete",
              "contact_phone_number": "7893877745",
              "description": "Description",
              "contact_name": "achari"
        })
        response = requests.put("http://localhost:5000/api/v1/events/2",headers={"Content-Type": "application/json"}, data=payload)
        response_body =response.json()
        # print("update response {}".format(response_body))
        content=response_body['response']
        assert response_body['status'] == '201'
        assert content["contact_name"] =="achari"
        assert content["contact_phone_number"] =="7893877745"

    def test_get_event_by_id(self):
        payload = json.dumps({
              "notes": "notes !!",
              "status": "Complete",
              "contact_phone_number": "7893877745",
              "description": "Description",
              "contact_name": "chinni"
        })
        response = requests.post("http://localhost:5000/api/v1/events",headers={"Content-Type": "application/json"}, data=payload)
        response_body =response.json()
        data=response_body["response"]
        id=data["id"]
        # print("get by id = {}".format(id))

        response = requests.get("http://localhost:5000/api/v1/events/{}".format(id),headers={"Content-Type": "application/json"})
        response_body =response.json()
        # print("get by id response {}".format(response_body))
        assert response_body["contact_name"] == "chinni"
        assert response_body["id"] == id

if __name__ == '__main__':
    unittest.main()