import imaplib
import re

def insertar_msg_en_txt(insertar):
    for id in insertar:
        file_msg.write(id + "\n")

def insertar_RPri_en_txt(insertar):
    for id in insertar:
        file_RPri.write(id + "\n")

def insertar_RPen_en_txt(insertar):
    for id in insertar:
        file_Rpen.write(id + "\n")
        
def insertar_utc_en_txt(insertar):
    for id in insertar:
        file_utc.write(id + "\n")
    
def find_Recibe(texto, param):
    pos = []
    contador = 0
    
    while contador != -1:
        contador = texto.find(param,contador)
        if contador != -1:
            pos.append(contador)
            contador += 1

    return pos
    
#datos
user = 'conisepulvedairigoin@gmail.com'
password = 'sbqikvwfwjgkloqe'
host = 'imap.gmail.com'
imap = imaplib.IMAP4_SSL(host)

imap.login(user, password)
imap.select('Inbox')
Emails = ['noreply@redditmail.com','noresponder@spdigital.cl','transaction@notice.aliexpress.com','contacto@mail.somosmach.com','latam@mail.latam.com']


for i in range(5):
    msg_id = list()
    receivedPrimero = list()
    receivedPenultimo = list()
    utc = list()
    contador_msg_id = 0
    contador_received = 0
    typ, data = imap.search(None,'FROM', Emails[i])

    for num in data[0].split():
        
        if(contador_msg_id <=40):
            #////////////////////MESSAGEid/////////////////////////////////////

            typ_msg_id, data_msg_id = imap.fetch(num, '(BODY[HEADER.FIELDS (Message-ID)])')
            datito_msg_id= data_msg_id[0][1].decode()
            datito_msg_id=datito_msg_id.replace("Message-ID:", "")
            datito_msg_id=datito_msg_id.replace(">", "")
            datito_msg_id=datito_msg_id.replace("<", "")
            datito_msg_id=datito_msg_id.replace("Message-Id:", "")
            datito_msg_id=datito_msg_id.strip()
            msg_id.append(datito_msg_id)
            
            #print(datito_msg_id)
            #////////////////////RECEIVED/////////////////////////////////////
        
            typ_recibe, data_recibe = imap.fetch(num, '(BODY[HEADER.FIELDS (Received)])')
            datito_recibe= data_recibe[0][1].decode()
            auxiliar=find_Recibe(datito_recibe,'Received:')
            #print(datito_recibe + str(contador_msg_id))
            ReceivedPrimero=datito_recibe[auxiliar[len(auxiliar)-1]:]
            receivedPrimero.append(ReceivedPrimero)
            if(len(auxiliar) > 2):
                Receivedpenultimo=datito_recibe[auxiliar[1]:auxiliar[len(auxiliar)-1]]
                receivedPenultimo.append(Receivedpenultimo)
            elif(len(auxiliar) == 2):
                Receivedpenultimo=datito_recibe[auxiliar[1]:]
                receivedPenultimo.append(Receivedpenultimo)
            else:
                Receivedpenultimo=datito_recibe[auxiliar[0]:]
                receivedPenultimo.append(Receivedpenultimo)

            #//////////////////////UTC///////////////////////////////////

            #print(ReceivedPrimero)
            auxiliar1utc=find_Recibe(ReceivedPrimero,' -')
            #print(contador_msg_id)
            if(len(auxiliar1utc)>0):
                a = ReceivedPrimero[auxiliar1utc[len(auxiliar1utc)-1]:]
                #print(a)
                if ' (' in a:
                    pos_a=a.index(' (')
                    a=a[:pos_a]
                    utc.append(a)
                else:
                    utc.append(a)
            elif len(auxiliar1utc) == 0:
                auxiliar1utc=find_Recibe(ReceivedPrimero,' +')
                a = ReceivedPrimero[auxiliar1utc[len(auxiliar1utc)-1]:]
                
                if ' (' in a:
                    pos_a=a.index(' (')
                    a=a[:pos_a]
                    utc.append(a)
                else:
                    utc.append(a)
            
            #/////////////////////////////////////////////////////////

            # typ_from, data_from = imap.fetch(num, '(BODY[HEADER.FIELDS (From)])')
            # datito_from= data_from[0][1].decode()
            # datito_from=datito_from.replace("From: ", "")
            # head, sep, tail = datito_from.partition(' <')
            # datito_from=head.strip()
            # datito_from=datito_from.strip('"')
            # datito_correo = tail.replace('>', '')
            #print("Este es el FROM: " + datito_from + " con correo: " + datito_correo)
            contador_msg_id += 1
    #print("EL contador de "+ Emails[i] +" los MSG_ID es " + str (contador_msg_id) + "\n")
    file_msg = open('msgID_'+ str(i) +'.txt', 'w')
    file_RPri = open('RPri_'+ str(i) +'.txt', 'w')
    file_Rpen = open('RPen_'+ str(i) +'.txt', 'w')
    file_utc = open('UTC_'+ str(i) +'.txt', 'w')
    insertar_msg_en_txt(msg_id)
    insertar_RPri_en_txt(receivedPrimero)
    insertar_RPen_en_txt(receivedPenultimo)
    insertar_utc_en_txt(utc)
imap.close()
file_msg.close()