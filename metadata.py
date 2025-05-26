LOCATION_OPTIONS = {
    "DARJEELING": [6, 1, 1, 2],
    "KALIMPONG": [6, 1, 1, 2],
    "JALPAIGURI": [1, 5, 1, 3],
    "ALIPURDUAR": [1, 5, 1, 3],
    "COOCHBEHAR": [4, 2, 2, 2],
    "MALDA": [1, 4, 2, 3],
    "UTTAR DINAJPUR": [3, 3, 2, 2],
    "DAKSHIN DINAJPUR": [2, 5, 2, 1],
    "MURSHIDABAD": [2, 3, 2, 3],
    "BIRBHUM": [4, 1, 2, 3],
    "HOOGHLY": [2, 3, 3, 2],
    "PASHCHIM BARDHAMAN": [1, 3, 4, 2],
    "PURBA BARDHAMAN": [1, 3, 3, 3],
    "BANKURA": [1, 4, 3, 2],
    "JHARGRAM": [1, 4, 3, 2],
    "PURULIA": [1, 4, 1, 4],
    "PURBA MEDINIPUR": [3, 1, 3, 3],
    "PASHCHIM MEDINIPUR": [3, 1, 4, 2],
    "HOWRAH": [2, 4, 3, 1],
    "KOLKATA": [1, 4, 4, 1],
    "NADIA": [1, 3, 3, 3],
    "NORTH 24 PARGANAS": [2, 3, 3, 2],
    "SOUTH 24 PARGANAS": [3, 1, 3, 3],
}

TIME = {
    "Early Morning": [3, 3, 3, 3],
    "During the day": [3.5, 3.5, 8.5, 1],
    "Evening": [8.5, 8.5, 4.5, 3],
    "Night": [6.5, 7.5, 3.5, 8.5],
}


SEASON = {
    "Monsoon": [9, 9, 7, 9],
    "Autumn": [7, 8.5, 8, 8.5],
    "Winter": [5.5, 5.5, 6.5, 5.5],
    "Spring": [7, 7, 7, 7.5],
    "Summer": [9, 9, 9, 9],
}


PLACE= {
    "Indoor": [3 , 7.5 , 6, 8.5],
    "Agriculture Field (Dry)":	[5.5 , 6.5, 9,	1],
    "Agriculture Field (Wet)/Near Water Bodies": 	[9	,4,	5.5,0.5],
    "High and Dry Areas (Near Human Settlements)-Outdoor":	[5	,8.5 ,7	,2.5],

       }


LOCAL_SYMPTOMS={
    "pain": [6, 6, 8, 1],
    "swelling": [4.5, 4.5, 6.5, 1],
    "haemmorhage": [4, 4, 7, 1],
    "skin colour change": [4, 4, 8, 0.5],
    "Blisters": [4, 4, 8, 0.5],
    "No Symptoms":[0,0,0,0],
}

SYSTEMATIC_SYMPTOMS={
"drowsiness": [6, 6, 1, 6.5],
"breathing difficulty": [6.5, 6.5, 2, 6.5],
"abdominal pain/vomiting": [2, 2, 1, 8.5],
"dropping eyes (ptosis)": [7, 7, 2, 8],
"swallowing issue/burning sensation in upper chest and throat": [7, 7, 1, 8],
"haemmorhage_systematic": [0.5, 0.5, 8, 0.5],
"paralysis": [7, 7, 1, 7],
"No Symptoms":[0,0,0,0],
}