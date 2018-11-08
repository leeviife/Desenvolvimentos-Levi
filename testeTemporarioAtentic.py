
import os, paramiko, csv, socket, pandas, time,datetime

op = 1
while(op != 1000):



    def ssh_check(ipAdress, ssh_username, ssh_password,ssh_enablepass):
      

        result = ""

        print("Connecting via SSH host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)
            stdin, stdout, stderr = ssh.exec_command('show inventory')
            ##tentando conectar com a senha de enable

            model = []
            
            for i in stdout.readlines():
                if "PID" in i:
                    model.append(i)
                    
            result = "OK",model


        except paramiko.ssh_exception.SSHException as error:
            
            result = ("Error",error)
        except (paramiko.ssh_exception.AuthenticationException):
            print("Erro de autenticacao neste equipamento")
            result = ("Error","SSH Authentication failed for some reason")
     
        except (socket.error):
            result = ("Error","SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()

        
        print(result)    

        return(result)


    def ssh_check_enable(ipAdress,ssh_username, ssh_password, ssh_enablepass):
 
        result = ""
        print("Querying values in host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)
            remote_conn = ssh.invoke_shell(term='vt100', width=800, height=500, width_pixels=0,height_pixels=0)

            ############### REALIZANDO A LINHA DE COMANDO NO EQUIPAMENTO ############
            command = "show running-config" ##executa o comando proprio do modo enable
            remote_conn.send(command + "\n")
                   #####ESSA ETAPA E NECESSARIA PARA O CASO DO EQUIPAMENTO SER ROOT OU NAO TER SENHA DE ENABLE
            time.sleep(.8)

            temp = str(remote_conn.recv(10000))##armazena o resultado recuperado numa variavel
            result = str("interface" in temp)##verificando se ha a palavra 'interface' localizada quando o comando e executado com exito

            if(result == "False"):##caso retorne falso, devido n`ao encontrar a palavra, ele entra no enable com senha

                remote_conn.send("enable\n\n\n\n")
                time.sleep(.2)
                print("chegou ate aquyu")
                command = "show running-config"##para verificar se o modo enable nao tem senha, caso o 

                temp = str(remote_conn.recv(10000))
                result = str("interface" in temp)
                print(result,"---resultado apos tentar enable sem sennha---")
                if(result == "False"):
                    

                    remote_conn.send("enable\n")
                    time.sleep(.2)
                    remote_conn.send(ssh_enablepass + "\n")
                    time.sleep(.8)
    
                    command = "show running-config"## A necessidade de executar este comando e para verificar se o modo enable est  on ou off
                    remote_conn.send(command + "\n")## pois no caso off o comando nao retorna exito
                        
                    time.sleep(.8)
                                    
                  


                    temp = str(remote_conn.recv(10000))
                    result = str("interface" in temp)
                    print(result,"---resultado apos inserir senha---")
                else:
                    print(result,"---resultado apos tentar enable sem sennha---")


        except (paramiko.SSHException):
            result = ("SSH Password is invalid!")
        except (paramiko.AuthenticationException):
            result = ("SSH Authentication failed for some reason")
        except (socket.error):
            result = ("SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()

            
        return(result)

    def ssh_check_running(ipAdress, ssh_username, ssh_password, ssh_enablepass):
     
        result = ""
        print("Querying values in host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)
            remote_conn = ssh.invoke_shell(term='vt100', width=800, height=500, width_pixels=0,height_pixels=0)

            ############### REALIZANDO A LINHA DE COMANDO NO EQUIPAMENTO ############
            remote_conn.send("enable\n")
            time.sleep(.2)
            remote_conn.send(ssh_enablepass + "\n")
            time.sleep(.8)
                
            command = "show running-config"
            remote_conn.send(command + "\n")
                   
            time.sleep(.8)
                            
            command = "show authentication sessions"
            remote_conn.send(command + "\n")
            time.sleep(.8)

            result = remote_conn.recv(10000)
        except (paramiko.SSHException):
            result = ("SSH Password is invalid!")
        except (paramiko.AuthenticationException):
            result = ("SSH Authentication failed for some reason")
        except (socket.error):
            result = ("SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()

            
        return(result)


    def ssh_check_startup(ipAdress, ssh_username, ssh_password, ssh_enablepass):
        
        
        result = ""
        print("Querying values in host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)
            remote_conn = ssh.invoke_shell(term='vt100', width=800, height=500, width_pixels=0,height_pixels=0)
            
            ############## REALIZANDO A LINHA DE COMANDO NO EQUIPAMENTO ##########
            remote_conn.send("enable\n")
            time.sleep(.2)
            remote_conn.send(ssh_enablepass + "\n")
            time.sleep(.8)
                
            command = "show startup-config"
            remote_conn.send(command + "\n")
                   
            time.sleep(.8)
                            
            command = "show authentication sessions"
            remote_conn.send(command + "\n")
            time.sleep(.8)

            result = remote_conn.recv(10000)
        except (paramiko.SSHException):
            result = ("SSH Password is invalid!")
        except (paramiko.AuthenticationException):
            result = ("SSH Authentication failed for some reason")
        except (socket.error):
            result = ("SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()

            
        return(result)


    def get_txt_file():
        txt_file_name = input("Por favor, informe um arquivo valido com as credenciais de acesso:\nNao se esqueca de colocar a extensao do arquivo\n ")
        full_path = os.path.abspath(txt_file_name)
    
     #print(full_path)
        if not os.path.isfile(full_path):
            print("Arquivo invalido!")
        #get_txt_file()
        else:
            return full_path
    def export_csv(result, csv_filetoexport):
    
        full_path = os.path.abspath(csv_filetoexport)
        
        (pandas.DataFrame.from_dict(data=result, orient='index') .to_csv(full_path + ".csv", header=False,sep=";"))
        print("The file has been saved in {}.csv.".format(full_path))

       
    ddlogo= """
           /\
                                                                              /__\        -------------------------------------------
         /\  /\      |           Dimension Data Brasil           |
        /__\/__\     |     Development intern - Automation       |
        DIMENSION    |          Script to backup config          |
        -----DATA     -------------------------------------------
                                       Writen by. Levi Teixeira
                                       V. 1.2
                                       
                                       """

    print(ddlogo)
   

    menuselector= """
        +++++++++  Backup Config - Automation Menu  +++++++++++++++
            -- Digite 1 para realizar o backup da Running-config com busca automatica de credenciais :
            -- Digite 2 para realizar o backup da Startup-config com busca automatica de credenciais :
            -- Digite 3 para fazer teste de autenticacao nos equipamentos:
            -- Digite "sair" para finalizar o processo.
                                       """

    print(menuselector)
    op = int(input("R: "))
    
        
    if (op == 1):

        print("")
        result={}
        count = 0
        ip_file = get_txt_file()


        f = csv.reader(open(ip_file), delimiter=';')
        for [ipAdress, ssh_username, ssh_password, ssh_enablepass] in f: 
            count += 1 
            sshtest = ssh_check(ipAdress,ssh_username, ssh_password, ssh_enablepass)
                
            if sshtest[0] == "OK":
                                
                returntext = ssh_check_running(ipAdress, ssh_username, ssh_password, ssh_enablepass)
                checkhour = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
                filetoexport = (" bkp_Running{0} _ {1}.txt").format(ipAdress,checkhour)
        
                file = open(filetoexport,"w") 
                file.write(returntext.decode('ascii'))
                file.write("\n")
                file.write("\n")
    
                file.close() 

                print("BACKUP DO EQUIPAMENTO REALIZADO COM SUCESSO!")    

                result= filetoexport   
                op = 0                           
                    
            else:
                result = ipAdress,sshtest[1]
    elif (op == 2):

        print("")
        result={}
        count = 0
            
        ip_file = get_txt_file()


        f = csv.reader(open(ip_file), delimiter=';')
        for [ipAdress, ssh_username, ssh_password, ssh_enablepass] in f: 
            count += 1 
        
            sshtest = ssh_check(ipAdress,ssh_username, ssh_password, ssh_enablepass)
                
            if sshtest[0] == "OK":
                                
                returntext = ssh_check_startup(ipAdress, ssh_username, ssh_password, ssh_enablepass)
                checkhour = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
                filetoexport = (" bkp_Startup{0} _ {1}.txt").format(ipAdress,checkhour)
        
                file = open(filetoexport,"w") 
                file.write(returntext.decode('ascii'))
                file.write("\n")
                file.write("\n")
    
                file.close() 

                print("BACKUP DO EQUIPAMENTO REALIZADO COM SUCESSO!")    

                result= filetoexport   
                op = 0                           
                    
            else:
                result = ipAdress,sshtest[1]
    elif (op == 3):

        print("")
        result={}
        count = 0
            
        ip_file = get_txt_file()
        nomeFile = ""
        while(nomeFile == ""):
            nomeFile = input("Digite o nome do arquivo a ser criado com o relatorio dos equipamentos:\n")
            
        filetoexport = ("Status_Authentication_{0}.txt").format(nomeFile)

        f = csv.reader(open(ip_file), delimiter=';')
        ##CUIDADO! NAO DEIXE LINHAS EM BRANCO NO ARQUIVO DE CREDENCIAIS, NEM APOS O ULTIMO REGISTRO
        for [ipAdress, ssh_username, ssh_password, ssh_enablepass] in f: 
            count += 1 
        
            sshtest = ssh_check(ipAdress,ssh_username, ssh_password,ssh_enablepass)
                                         
            sshenable = ssh_check_enable(ipAdress,ssh_username, ssh_password,ssh_enablepass)
            saidaOk = ("{0} Authentication OK").format(ipAdress)
            saidaFail = ("{0} Authentication FAILED").format(ipAdress)
            saidaEnableOk = ("{0} Pass Enable OK\n****************").format(ipAdress)
            saidaEnableFail = ("{0} Pass Enable FAILED\n****************").format(ipAdress)
            lista=[]
            if sshtest[0] == "OK":
                lista.append(saidaOk)
                if (sshenable == "True"):
                    lista.append(saidaEnableOk)
                    str(lista)
                else:
                    lista.append(saidaEnableFail)
                    str(lista)
            else:
                lista.append(saidaFail)
                str(lista)
            print("STATUS DE AUTENTICACAO DO EQUIPAMENTO REALIZADO COM SUCESSO!")    
            print(lista)
##            file = open(filetoexport,"a") 
##            file.write(lista)
##            file.write("\n")
##            file.close()

            with open(filetoexport, 'a') as f:##nao pode ter aquivos de backup com o mesmo nome pois neste caso ele faz um for onde ele atualiza acrescentando linhas no 
                ## o respectivo nome do 'fileexport' 
                for s in lista:
                    f.write(str(s) + '\n')
            result= filetoexport   
            op = 0                           
                    
    else:
        print("Opcao invalida!")
