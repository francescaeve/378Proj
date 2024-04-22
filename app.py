from vetiver import VetiverModel
from dotenv import load_dotenv, find_dotenv
import vetiver
import pins

load_dotenv(find_dotenv())

b = pins.board_folder('/data/model', allow_pickle_read=True)
v = VetiverModel.from_pin(b, 'penguin_model', version = '20240416T100728Z-a6f9b')

vetiver_api = vetiver.VetiverAPI(v)
api = vetiver_api.app

@reactive.Calc
def vals():
  d = {
    "bill_length_mm" : input.bill_length(),
    "sex_male" : input.sex() == "Male",
    "species_Gentoo" : input.species() == "Gentoo", 
    "species_Chinstrap" : input.species() == "Chinstrap"
  }
  return d

  @reactive.Calc
  @reactive.event(input.predict)
  def pred():
    r = requests.post(api_url, json = [vals()])
    return r.json().get('predict')[0]
  
  
import logging
logging.basicConfig(
  format='%(asctime)s - %(message)s',
  level=logging.INFO
)
logging.info("App Started")

logging.info("Request Made")
r = requests.post(api_url, json = [vals()])
logging.info("Request Returned")

if r.status_code != 200:
  logging.error("HTTP error returned")
  
return r.json().get('predict')[0]

