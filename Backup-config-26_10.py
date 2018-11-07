import os, paramiko, socket, pandas, time,datetime ##importações necessárias, os frameworks devem ser instalados antes da execução.

op = 1;

while(op != 1000):##laço para retornar ao menu sempre que uma opção válida é executada, e sair com a entrada 1000
    def ssh_check(ipAdress, ssh_username, ssh_password): ##função de conexão com os parâmetros necessários, advindos da entrada do usuário após o menu
      
        result = ""
        print("Connecting via SSH host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()##cria representação de uma sessão com um servidor SSH
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())##define a política que SSHClient deve ser usada quando o nome do host do servidor SSH não estiver nas chaves do host do sistema ou nas chaves do aplicativo.
        try:##tente
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)##tenta conectar usando os parâmetros 
            stdin, stdout, stderr = ssh.exec_command('show inventory')

            model = []
            
            for i in stdout.readlines():##passando pelas linhas do stdin exibidas pelo show inventory
                if "PID" in i:##verificando se há um identificador de processo nesse show inventory pra resultar o OK
                    model.append(i)

            result = "OK",model
        except paramiko.ssh_exception.SSHException as error:##resultando erros
            
            result = ("Error",error)
        except (paramiko.ssh_exception.AuthenticationException):
            result = ("Error","SSH Authentication failed for some reason")
     
        except (socket.error):
            result = ("Error","SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()
            
        return(result)


    def ssh_check_running(ipAdress, ssh_username, ssh_password, ssh_enablepass):##função de check running, com as variáveis de referencia como parâmetro
     
        result = ""
        print("Querying values in host IP {0}.".format(ipAdress))
            
        ssh = paramiko.SSHClient()##inicia novamente uma sessão com o servidor SSH
       
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())##definindo de novo a politica quando o nome de host do SSH está ausente
        try:
            ssh.connect(ipAdress, username=ssh_username, password=ssh_password)##conectando ...
            remote_conn = ssh.invoke_shell(term='vt100', width=800, height=500, width_pixels=0,height_pixels=0)##invocando o shell command

            ############### REALIZANDO A LINHA DE COMANDO NO EQUIPAMENTO ############
            remote_conn.send("enable\n")##enviando comando
            time.sleep(.2)##dando tempo pro comando processar
            remote_conn.send(ssh_enablepass + "\n")##inserindo a senha de enable e quebrando linha
            time.sleep(.8)##dando um tempo maior de processamento
            ## executando os demais comandos    
            command = "show running-config"
            remote_conn.send(command + "\n")
                   
            time.sleep(.8)
                            
            command = "show authentication sessions"
            remote_conn.send(command + "\n")
            time.sleep(.8)
            
            result = remote_conn.recv(10000)##recupera os comandos armazenados no remote_conn com um limite de 10000 linhas
        except (paramiko.SSHException):##retornando erros
            result = ("SSH Password is invalid!")
        except (paramiko.AuthenticationException):
            result = ("SSH Authentication failed for some reason")
        except (socket.error):
            result = ("SSH Socket connection failed on {0}!".format(ipAdress))
        ssh.close()##fechando conexao ssh
            
        return(result)##retornando os resultados


    def ssh_check_startup(ipAdress, ssh_username, ssh_password, ssh_enablepass):##função de execução da startup config, com os mesmos procedimentos         
        
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


    
    ddlogo= """
           /\
                                                                              /__\        -------------------------------------------
         /\  /\      |           Dimension Data Brasil           |
        /__\/__\     |     Development intern - Automation       |
        DIMENSION    |          Script to backup config          |
        -----DATA     -------------------------------------------
                                       Writen by. Levi Teixeira
                                       V. 1.0
                                       
                                       """

    print(ddlogo)
   
    menuselector= """
        +++++++++  Backup Config - Automation Menu  +++++++++++++++
            -- Digite 1 para realizar o backup da Running-config:
            -- Digite 2 para realizar o backup da Startup-config:
            -- Digite 1000 para sair

                                       """
    print(menuselector)
    op = int(input("R: "))
        
    if (op == 1):##condicional usando a opção inserida acima na var OP

        print("")
        result={}
        ##entrando com as informações de autenticação
        ipAdress=input("Digite o IP do equipamento a fazer o backup:\n")
        ssh_username=input("Digite o USERNAME do equipamento:\n")
        ssh_password=input("Digite o PASSWORD do equipamento:\n")
        ssh_enablepass=input("Digite a senha de enable:\n")
    
        sshtest = ssh_check(ipAdress,ssh_username, ssh_password)##trazendo todo o resultado da conexão aqui, para executar as sub condicionais se a conexão for OK
               
        if sshtest[0] == "OK":
                               
            returntext = ssh_check_running(ipAdress, ssh_username, ssh_password, ssh_enablepass)##armazenando o result da running na variavel return text
            checkhour = datetime.datetime.now().strftime("%y-%m-%d-%H-%M") ##formatando o horario e data
            filetoexport = (" bkp_Running{0} _ {1}.txt").format(ipAdress,checkhour)##formatando o nome do arquivo
      
            file = open(filetoexport,"w") ##criando e escrevendo(w) no arquivo 
            file.write(returntext.decode('ascii'))##escrevendo no arquivo todo o return text da running check
            file.write("\n")
            file.write("\n")
            file.close() ##fechando o arquivo

            print("BACKUP DO EQUIPAMENTO REALIZADO COM SUCESSO!")    

            result= filetoexport   
            op = 0       ##zerando a opção                    
                
        else:
            result = ipAdress,sshtest[1]
    elif (op == 2):## caso 2, mesmos processos acima, porém chamando a startup check

        print("")
        result={}
        
        ipAdress=input("Digite o IP do equipamento a fazer o backup:\n")
        ssh_username=input("Digite o USERNAME do equipamento:\n")
        ssh_password=input("Digite o PASSWORD do equipamento:\n")
        ssh_enablepass=input("Digite a senha de enable:\n")
    
        sshtest = ssh_check(ipAdress,ssh_username, ssh_password)
               
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
    else:
        print("Opcao invalida!")
        
  


