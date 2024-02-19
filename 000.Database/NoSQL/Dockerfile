FROM leafney/alpine-mongo-tools

ARG USER_ID=iftbigdata
ENV USER_ID $USER_ID

# make docker local directory home
RUN mkdir /home/${USER_ID}/ 

# load Mongodb
COPY CourseworkOne.json /home/${USER_ID}/
COPY CourseworkOne.json /home/${USER_ID}/

CMD mongoimport --uri mongodb://mongo_db_cw:27017/Equity --collection CourseworkOne --drop --file /home/${USER_ID}/CourseworkOne.json --jsonArray
