import os
class symbol():
    def __init__(self, name, cat):
        self.name = name
        self.cat = cat      

class variable(symbol):
    def __init__(self, fname, type, scope, valor = '', cat = 'variable'):
        super().__init__(fname, cat)
        self.type = type
        self.scope = scope
        self.valor =  valor   

class funcion(symbol):
    def __init__(self, fname, type, cat = 'funcion'):
        super().__init__(fname, cat)
        self.type = type

    def insert_args(self, var):
        self.args.append(var)   
     
class SymbolTable():
    def __init__(self):
        self._symbols = dict()
        self.error_list = []
        self.types = ['int', 'void', 'string', 'float']
        self.opers = ['+', '-', '*', '/', '%']
        self.keywords = ['if', 'while', 'return']
        self.scoping = []

    def __str__(self):
        header = 'SymbolTable \n'
        columns = '|{:9}|{:9}|{:9}|{:9}|{:9}|\n'.format('name', 'category', 'type', 'scope', 'value')
        hline = '-' * (len(columns)-1) + '\n'
        s = header + hline + columns + hline

        for key, value in  self._symbols.items():
            if value.cat == 'variable':
                s += "|{:9}|{:9}|{:9}|{:9}|{:9}|\n".format(key, value.cat, value.type, value.scope, str(value.valor).strip())
            else:
                s += "|{:9}|{:9}|{:9}|{:9}|{:9}|\n".format(key, value.cat, value.type, "null", 'null')
        s += hline
       
        return s
    __repr__= __str__

    def insert(self, symbol):
        if symbol.type == 'variable':
            self._symbols[symbol.name] = symbol
            return
        self._symbols[symbol.name] = symbol
    
    def lookup(self, name):
        symbol = self._symbols.get(name)
        return symbol

    def revision(self, var, valor):
        if(self.lookup(var).type == 'variable'):
            if (self.lookup(var).type == tipos_var[0] and type(valor) is not int or
                self.lookup(var).type == tipos_var[1] and type(valor) is not float or
                self.lookup(var).type == tipos_var[2] and type(valor) is not string):
                return False 
            else: return True
            
    def value_concerns(self, num, linea, var):
        sym = self.lookup(var)
        if '=' not in linea:
            if self.lookup(linea[0]).cat == 'funcion':
                lineaP = linea[1:]
                aux = len(lineaP)
                c = 0
                t = None
                tmp = list(self._symbols.keys())[list(self._symbols.keys()).index(linea[0])+1:]
                for i in range(aux):
                    if(type(eval(lineaP[i])) == float): t = self.types[3]
                    if(type(eval(lineaP[i])) == int): t = self.types[0]
                    if(type(eval(lineaP[i])) == str): t = self.types[2]
                    if t != self.lookup(tmp[i]).type:
                        self.error_list.append("Error –- Linea {}: Parámetro de tipo incorrecto en la función '{}'.".format(num, var))
                        return
                return
            else:
                self.error_list.append("Error –- Linea {}: No se hace una asignación correcta a la variable.".format(num, var))
                return
        if var not in self._symbols.keys():
            self.error_list.append("Error –- Linea {}: No existe la variable.".format(num))
            return
        if '=' in linea:
            linea2 = linea[linea.index('=')+1:]

        if sym.type == self.types[0]:
            for key in self._symbols.keys():
                if key in linea2:
                   if sym.type == self.lookup(key).type and type(sym.valor) == type(self.lookup(key).valor):
                       linea2 = [str(self.lookup(key).valor) if x==key else x for x in linea2]
                   else:
                       self.error_list.append("Error –- Linea {}: La variable '{}' y la variable '{}' son de diferente tipo y no se pueden realizar operaciones entre ellas.".format(num, sym.name, self.lookup(key).name))   
                       return  
            
            aux = ''.join(linea2)
            try:
                if aux == '': 
                    value = None
                else:
                    value = int(eval(aux))
            except: 
                self.error_list.append("Error –- Linea {}: A la variable '{}' que es de tipo {} se le asigna un valor de un tipo incorrecto.".format(num, var, sym.type))
                return
            sym.valor = value       
        if sym.type == self.types[1]:
            self.error_list.append("Error –- Linea {}: A la variable '{}' es de tipo void, no es posible asignarle valores.".format(num, var))
            return

        if sym.type == self.types[2]:
            for key in self._symbols.keys():
                if key in linea2:
                    if self.lookup(key).cat == 'funcion':
                        if self.lookup(key).type == sym.type:
                            func = self.lookup(key)
                            break
                        else:
                            self.error_list.append("Error –- Linea {}: La variable '{}' y la función '{}' no coinciden.".format(sym.name, self.lookup(key).name))  
                            return
                    if sym.type == self.lookup(key).type and type(sym.valor) == type(self.lookup(key).valor):
                        linea2 = [str(self.lookup(key).valor) if x==key else x for x in linea2]
                    else:
                        if self.lookup(linea2[0]).cat == 'funcion' and self.lookup(linea2[0]).type == sym.type: 
                            return
                        else:
                            self.error_list.append("Error –- Linea {}: La variable '{}' y la variable '{}'  son de diferente tipo y no se pueden realizar operaciones entre ellas.".format(sym.name, self.lookup(key).name))   
                            return
            if linea2[-1] in self._symbols.keys():
                if self.lookup(linea2[-1]).scope != "global":
                    self.error_list.append("Error –- Linea {}: La variable '{}' no tiene alcance global.".format(num, linea2[-1]))   
                    return 
            value = ''.join(linea2)
            if '"' in value:
                sym.valor = value
            
            else:
                self.error_list.append("Error –- Linea {}: A la variable '{}' que es de tipo {} se le asigna un valor de un tipo incorrecto.".format(num, var, sym.type))
                return
        if sym.type == self.types[3]:
            for key in self._symbols.keys():
                if key in linea2:
                    print()
                    if sym.type == self.lookup(key).type and type(sym.valor) == type(self.lookup(key).valor):
                        linea2 = [str(self.lookup(key).valor) if x==key else x for x in linea2]
                    else:
                        self.error_list.append("Error –- Linea {}: La variable '{}' y la variable '{}' son de diferente tipo y no se pueden realizar operaciones entre ellas.".format(num, sym.name, self.lookup(key).name))   
                        return
            aux = ''.join(linea2)
            try:
                if aux == '': 
                    value = None
                else:
                    value = float(eval(aux))
            except: 
                self.error_list.append("Error –- Linea {}: A la variable '{}' que es de tipo {} se le asigna un valor de un tipo incorrecto.".format(num, var, sym.type))
                return 
            sym.valor = value
        if self.revision(var, value):
            self.error_list.append("Error –- Linea {}: A la variable '{}' se le asigna un valor que no coresponde a su tipo".format(num, var))
        return
    
    def creation(self, num, linea, tipovar):
        #creacion de simbolos e 
        scoper = None
        for key in self._symbols.keys():
            if self.lookup(key).cat == 'funcion':
                scoper == 'local'
        if len(self.scoping):
            scoper = 'local'
        elif '{' in self.scoping: 
            scoper = 'local'
        else: 
            scoper = 'global'
        if linea[1] in self._symbols.keys():
             self.error_list.append("Error –- Linea {}: La variable '{}' ya está definida. No se acepta redefinición.".format(num, linea[1]))
             return
        if linea[-1] == '{':
            self.scoping.append(linea[-1])
            self.insert(funcion(linea[1], linea[0]))
            linea2 = linea[2:-1]
            for i in range(len(linea2)):
                if linea2[i] in self.types:
                   self.insert(variable(linea2[i+1], linea2[i], 'local'))  
        else:
            self.insert(variable(linea[1], tipovar, scoper))
            if '=' in linea:
                self.value_concerns(num, linea, linea[1])          
            else: return
        return

    def query(self, linea, num):
        _var = self.lookup(linea[1])  
        tipo = None
        if _var == None:
            _var = linea[1]
        if type(_var) == str: tipo = 'string'
        func = None
        for name in self._symbols.keys():
            if self.lookup(name).cat == 'funcion':
                func = self.lookup(name)
                break
        if func == None:
            self.error_list.append("Error –- Linea {}: No hay una función definida que permita hacer 'return'.".format(num))
            return
        elif func != None:
            if tipo:
                if (_var == linea[1] and (func.type != tipo)):
                    self.error_list.append("Error –- Linea {}: El tipo de retorno de la función '{}' no coincide con el tipo definido den su declaración.".format(num,func.name))
                    return
                else: return
            else: 
                if (_var == linea[1] and (func.type != type(_var))):
                    self.error_list.append("Error –- Linea {}: El tipo de retorno de la función '{}' no coincide con el tipo definido en su declaración.".format(num,func.name))
                    return
                elif (func.type != _var.type):           
                    self.error_list.append("Error –- Linea {}: El tipo de retorno de la función '{}' no coincide con el tipo definido en su declaración.".format(num,func.name))
                    return
                else: return
        
            

    def analizer(self, filename):
        import re        
        dirname = os.path.dirname(__file__)
        count = 0
        with open(dirname+'\\'+filename, 'r', encoding="utf8") as file:
            for line in file:
                count +=1
                line.strip()
                line = re.split(r"[ ;,()\n]+", line)   
                if line[0] == '':
                    line = line[1:]
                if line[-1] == '':
                    line = line[:-1]

                if line[0] in self._symbols.keys():
                    self.value_concerns(count, line, line[0])                    
                elif line[0] in self.types:
                    self.creation(count, line, line[0])
                elif line[0] == '}':
                    self.scoping.append(line[0])
                elif line[0] in self.keywords:
                    if line[0] in self.keywords[:-1]:
                        self.scoping.append(line[0])
                        self.scoping.append(line[-1])
                    elif line[0] in self.keywords[-1]:
                        self.query(line, count)
                else:
                    self.error_list.append("Error –- Linea {}: La línea inidicada no es reconocida.".format(count))
        file.close()
        if (self.scoping.count('{') + self.scoping.count('}')) % 2:
            self.error_list.append("Error –- Linea {}: Los brackets '{{}}' están incompletos.".format(count))
        if not len(self.error_list): print("No errors. Build Successful.")
        for error in self.error_list:
            print(error)

    def token(self, filename):
        print("\n Revisión de archivo: {}\n".format(filename))
        dirname = os.path.dirname(__file__)
        count = 0
        with open(dirname+'\\'+filename, 'r', encoding="utf8") as file:
            for line in file:
                count +=1
                print("{:2}:  {}".format(count, line), end="")
        print("\n\nLista de errores: ")
        file.close()
       
       
"""
Proyecto II. Analizador semántico.
Elaborado por:
> Joaquín Barrientos Monge
> Pablo Gatgens Chaves
20 noviembre 2020

"""
symt = SymbolTable()
symt.token('incorrecto.txt')
symt.analizer('incorrecto.txt')


symt2 = SymbolTable()
symt2.token('correcto.txt')
symt2.analizer('correcto.txt')

input()
