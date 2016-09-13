import re
class db(object):
    def __init__(self, file_name = None):
        self._file_name = file_name
        self._elements = {}
        self._attrs = []
    def set_filename(self, file_name):
        self._file_name = file_name
    def get_attrs(self):
        return self._attrs
    def get_elements(self):
        return self._elements
    def get_all_values(self):
        return self._elements.values()
    def get_from_key(self, keys, dic = None):
        if not dic:
            dic = self._elements
        if type(keys) == list:
            return [dic[key] for key in keys]
        if type(keys) == str:
            return dic[keys]
    @staticmethod
    def get_from_keys(self, keys, dic = None):
        if not dic:
            dic = self._elements
        return [dic[key] for key in keys]
    
    def clear(self):
        print('Clearing database...')
        self._elements.clear()
        print('Done...')
    #def _filter(self, attr, value, lst):
    #    print('filtering: %s == %s' % (attr, value))
    #    return [x for x in lst if x[attr] == value]
    #def _filter_contain(self, attr, value, lst):
    #    print('filtering: %s in %s' % (value,attr))
    #    return [x for x in lst if value in x[attr]]   
    #def _filter_re(self, attr, value, lst):
    #    print('filtering: %s match %s' % (value,attr))
    #    return [x for x in lst if re.match(value , x[attr])]  
    def fetch(self, attrs = [], values = [], method = 1, keys = None, dic =None):
        """Fetch elements from a dictionary.

        Args:
            attrs: list of dictionary keys for constraint. Empty list for no constraint.
            values: values corresponding to the keys for constraint. Empty list for no constraint.
            method:  1, 2 and else represent containment-, equivalent-, re- mode, respectively.
            lst: source dictionary. None indicate self._element.
            
         Return:
             dictionary of dictionary.
        """ 
        
        
        if not dic:
            dic = self._elements
        if not keys:
            keys = dic.keys()
        elif not set(keys) <= dic.keys():
            print('keys is not in dictionary')
            return []
        for i in range(len(attrs)):
            #print(i,attrs[i], values[i])
            if method == 1:
                #equivalent mode
                #print('filtering: %s == %s' % (attrs[i], values[i]))
                keys = [x for x in keys if dic[x][attrs[i]] == values[i]]
            elif method == 2:
                #containment mode
                #print('filtering: %s in %s' % (values[i], attrs[i]))
                keys = [x for x in keys if values[i] in dic[x][attrs[i]]] 
            else:
                #re mode
                #print('filtering: %s match %s' % (attrs[i], values[i]))
                keys = [x for x in keys if re.match(values[i] , dic[x][attrs[i]])]  
        return keys

        
    def set(self, element, attr, value):
        element[attr] = value
        return
    def add(self, key, attrs, values):
        temp ={}
        if len(attrs) == len(values):
            for i in range(len(attrs)):
                self.set(temp, attrs[i], values[i])
            #print(temp)
            self._elements[key] = temp
        else:
            print('The numbers of attributions(%d) and values(%d) are not equal to each other' % (len(attrs), len(values)))
        return
    def delete(self, key):
        if key in self._elements:
            self._elements.pop(key)
            print('Deleted...')
        else:
            print('No corresponding element')
        return
    def show(self, keys = None, dic = None, col_name = None):
        if not col_name:
            col_name = self._attrs
        if not dic:
            dic = self._elements
        if not keys:
            keys = dic.keys()
        elif not set(keys) <= dic.keys():
            print('keys is not in dictionary')
            return
            
        output = ''
        for key in keys:
            for col in col_name:                
                try:                    
                    output += '  %s: %s\n' % (col, dic[key][col])
                except KeyError:
                    continue
            if 'Location' in dic[key]:
                output += "    ==> " + str(dic[key]['Location']) + '\n'
            output += '\n'
        output +='='*80 + '\n'
        output += 'Total: %d'%len(keys)
        print(output)
        return
        
            
    
class SCH_db(db):
    def __init__(self, file_name = None, comp_file=None):
        self._file_name = file_name
        self._comp_file = comp_file
        self._head = None
        self._elements = {}
        self._comp_ref = {}
        self._attrs = []
        self._op_name = []
        self.SCH_type = ''
        self._keyname = '#Reference'
        self._op_key = '~op'
        self._page_key = '~page'
        self._design_key = '~design'
        self.comp_parsed = False
    def set_comp_file(self, comp_file):
        self._comp_file = comp_file
    def clear(self):
        print('Clearing SCH database...')
        self._head = None
        self._elements.clear()
        self._comp_ref.clear()
        self._attrs = []
        self._op_name = []
        self.SCH_type = ''
        self.comp_parsed = False
        print('Done...')
    def getkey(self):
        return self._keyname
    def setkey(self, value):
        self._keyname = value
        return
    def get_op_key(self):
        return self._op_key
    def set_op_key(self, value):
        self._op_key = value
        return
    def get_page_key(self):
        return self._page_key
    def set_page_key(self, value):
        self._page_key = value
        return
    def get_design_key(self):
        return self._design_key
    def set_design_key(self, value):
        self._design_key = value
        return    
    def _comp_add(self, key, value):
        if key in self._comp_ref:

            self._comp_ref[key][self.get_design_key()].append(value[1])
        else:
            #print(value)
            self._comp_ref[key] = {self.get_page_key(): value[0], self.get_design_key(): [value[1]]}
            
            
        return
        
    def parser(self):        
        self.clear()
        option_str = "^/+"
        if self._comp_file:
            #{Reference Number: [page_info ,[designators]]}
            #ex. U1A, U1B, U1C ---> {U1: [001. Test, [A,B,C]]}
            try:
                with open(self._comp_file) as f:
                    head = f.readline().replace('\n', '')
                    #print(head)
                    if head.split('\t')[:3] != ['Reference','', 'Designator']:
                        print('Undefined input: %s'%head.split('\t')[:3])
                        return
                    occ_count = 0
                    # useless. just for avoiding compiler error
                    inst_key = page = design =''
                    for line in f:
                        temp = line.replace('\n', '').split('\t')

                        if temp[1][0] != '/':
                            if occ_count == 0 and len(self._comp_ref) != 0:
                                self._comp_add(inst_key, [page, design])
                            
                            page =  ':'.join(temp[1].split(':')[:-1])
                            inst_key = temp[0]
                            design = temp[2]
                            occ_count = 0
                        else:
                            occ_count += 1
                            self._comp_add(temp[0], [page, temp[2]])
                self.comp_parsed = True
                print("Comp-file parsing done...Total: %d elements" % len(self._comp_ref))            
            except IOError:
                print('No corresponding file: %s' % self._comp_file)
                
                    
        try:
            with open(self._file_name, 'r') as f:
                f.readline()
                f.readline()
                #Occr or inst
                #self.SCH_type =  values[0].split(':')[0]
                self.SCH_type = f.readline().replace('\n', '').replace('"', '').split('\t')[0].split(':')[0]
                print(self.SCH_type)
                
                
            with open(self._file_name, 'r') as f:
                self._head = f.readline()
                self._attrs = f.readline().replace('\n', '').replace('"', '').split('\t');
                
                if self.getkey() in self._attrs:
                    print()
                    print('It is not a good idea to use %s as an attribution' % self.getkey())
                    print('Maybe you should change the key_name: %s'%self._keyname)
                    print()
                    # Change the keyname
                    return
                if self.get_op_key() in self._attrs:
                    print()
                    print('It is not a good idea to use %s as an attribution' % self.getkey())
                    print('Maybe you should change the op_key: %s'%self._keyname)
                    print()
                    # Change the op_key
                    return
                if self.get_page_key() in self._attrs:
                    print()
                    print('It is not a good idea to use %s as an attribution' % self.getkey())
                    print('Maybe you should change the page_key: %s'%self._keyname)
                    print()
                    # Change the page_key
                    return
                if self.get_design_key() in self._attrs:
                    print()
                    print('It is not a good idea to use %s as an attribution' % self.getkey())
                    print('Maybe you should change the design_key: %s'%self._keyname)
                    print()
                    # Change the design_key
                    return
                
                #self._attrs should not be altered because it will useful in Exporting!
                attrs = self._attrs[:]

                
                # find the positions of optional
                op_flag = []
                
                for index in range(len(self._attrs)):
                    if self._attrs[index].lower() == 'optional':
                        op_flag.append(index)
                        self._op_name.append(self._attrs[index])
                attrs.append(self.get_op_key())
                attrs.append(self.getkey())
                
                
                # find the position of 'part reference' or 'ID'
                if self.SCH_type == 'PARTOCC':
                    try:
                        PR_flag = self._attrs.index('Part Reference')
                    except ValueError:
                        print("It need 'Part Reference' in EXP")
                        return
                    
                    if not self._comp_file:
                        print()
                        print('######################')
                        print('NOTE:')
                        print('It is better to prepare comp-file for Occurrence-EXP')
                        print('######################')
                        print()
                        
                        
                else:
                    try:
                        PR_flag = self._attrs.index('ID')
                    except ValueError:
                        print("It need 'ID' in EXP")
                        return
                attrs.append(self.get_page_key())



                for i in f:
                    values = i.replace('\n', '').replace('"', '').split('\t');
                    
                    #modified key_flag in occurrence-EXP
                    #ex. U1A, U1B.... --> U1
                    #if U1 in _comp_ref & A in _comp_ref[U1]
                    #     key = U1A[:-1]
                    if self.SCH_type == 'PARTOCC' and self._comp_file:
                        if (values[PR_flag][:-1] in self._comp_ref
                            and values[PR_flag][-1] in self._comp_ref[values[PR_flag][:-1]][self.get_design_key()]):
                            
                            key = values[PR_flag][:-1]
                            self._comp_ref[key][self.get_design_key()].remove(values[PR_flag][-1])
                        elif values[PR_flag] in self._comp_ref:
                            key = values[PR_flag]
                        else:
                            print('Incorresponding between comp-file & EXP: %s' % values[PR_flag])
                            return
                            
                    else:
                        key = values[PR_flag]
                        
                        
                    
                    
                    #Duplication key --> clear and return
                    if key in self._elements:
                        if values[PR_flag] == self._elements[key]['Part Reference']:
                            
                            print('Duplication Reference: %s already in database...'% key)
                            self.clear()
                            return
                        else:
                            continue
                    
                    #~op 1: N/A.... 0: /x, /
                    op = True
                    for op_index in op_flag:
                        op = not re.match(option_str, values[op_index])
                        if not op:
                            break
                    values.append(op)
                    
                    values.append(key)


                    #page
                    if self.SCH_type == 'PARTINST':
                        page = ':'.join(values[0].split(':')[1:3])
                        values.append(page)
                    elif not self.comp_parsed:
                        values.append('------')
                    else:
                        values.append(self._comp_ref[key][self.get_page_key()])
                        
                    self.add(key.upper(), attrs, values)
                    #print(values[key_flag])
                #Occr or inst
                #self.SCH_type =  values[0].split(':')[0]
                #print(key)

            print("EXP parsing done...Total: %d elements" % len(self._elements))
            self.parserd = True
        except IOError:
            print('No corresponding file: %s' % self._file_name)
        return
    def get_op_name(self):
        return self._op_name
    def export(self):
        print('Exporting to %s...' % self._file_name)
        with open(self._file_name, 'w') as f:
            f.write('%s' % self._head)
            f.write('"%s"\n' % '"\t"'.join(self._attrs))
            
            for i in self._elements.values():
                
                f.write(('"%s"\n' % '"\t"'.join([i[j] for j in self._attrs])))
        return
    def print_SCH(self, col_name = None, attrs = [], values = [], method = 1,keys = None, dic = None):
        """Fetch and print elements from a dictionary.

        Args:
            col_name: list of keys for output style. Default self._attrs
            attrs: list of dictionary keys for constraint. Empty list for no constraint.
            values: values corresponding to the keys  for constraint. Empty list for no constraint.
            method: 0, 1(default), 2 represent containment-, equivalent-, re- mode, respectively.
            lst: source dictionary. None(default) indicate self._element.
            
         Return:
             None
        """

        
        keys = self.fetch(attrs, values, method,keys, dic)
        self.show(keys,dic, col_name)

    
class BOM_db(db):
    def __init__(self, file_name = None):
        self._file_name = file_name
        self._elements = {}
        #self._attrs = ['Part Number', 'Component_Name', 'Location']
        self._attrs = ['Part Number', 'Component_Name']
        self._attrs_res = ['Part Number', 'Value', 'PCB Footprint', 'Tolerance']
        self._attrs_cap = ['Part Number', 'Value', 'PCB Footprint', 'CType', 'CChar', 'Tolerance']
        #self._type = {'Res':set({}), 'Cap': set({}), 'Other': set({})}
        self._location ={}
    def clear(self):
        print('Clearing BOM database...')
        self._elements.clear()
        self._location.clear()
        print('Done...')
    def get_from_location(self, key):
        return self._location[key]

    def get_locations(self):
        return self._location
    
    def location_update(self, key, value):
        if key in self._location:
            raise Exception('Duplication')
        else:
            self._location[key] = value
    def parser(self):
        try:
            
            with open(self._file_name, 'r') as f:
                self.clear()
                for line in f:
                    if line == '\n':
                        break
                    
                    values = line[:-1].split('|')
                    #Duplication element
                    if values[0] in self._elements:
                        for location in f.readline()[:-1].split('|'):
                            self._elements[values[0]]['Location'].append(location)
                            try: 
                                self.location_update(location, values[0])
                            except:
                                print('Duplication location: %s'% location)
                    #New element
                    else:
                        attrs = self._attrs[:]                    
                        attrs.append('Component type')
                        if re.match('11G', values[0]):
                            attrs += self._attrs_cap[1:]
                            values.append('cap')
                            values += self.decode_mlcc(values[1])
                            #self._type['Cap'].add(values[0])
                        elif re.match('10G', values[0]):
                            attrs += self._attrs_res[1:]
                            values.append('res')
                            values += self.decode_res(values[1])
                            #self._type['Res'].add(values[0])
                        else:
                            values.append('other')
                            #self._type['Other'].add(values[0])
                        attrs.append('Location')
                        values.append(f.readline()[:-1].split('|'))
                        for location in values[-1]:
                            try: 
                                self.location_update(location, values[0])
                            except:
                                print('Duplication location: %s'% location)
                        
                        self.add(values[0], attrs, values)
            
            print('BOM parsing done...')
        except IOError:
            print('No corresponding file: %s' % self._file_name)
        return 
    def print_BOM(self, type_flag = '',attrs = [], values = [], col_name = [], method = 1, keys = None, dic =None):
        """Fetch and print elements from a dictionary.

        Args:
            type_flag: 'cap', 'res' and 'other' for cap, res and other type of elements, respectively. Other inputs(default) indicate all type of elements.
            attrs: list of dictionary keys for constraint. Empty list for no constraint.
            values: values corresponding to the keys for constraint. Empty list for no constraint.
            method: 0, 1(default), 2 represent containment-, equivalent-, re- mode, respectively.
            lst: source dictionary. None(default) indicate self._element.
            
         Return:
             None
        """

        if not col_name:
            if type_flag.lower() == 'cap':
                col_name = self._attrs_cap
                type_flag = 'cap'
            elif type_flag.lower() == 'res':
                col_name = self._attrs_res
                type_flag = 'res'
            elif type_flag.lower() == 'other':
                col_name = self._attrs
                type_flag = 'other'
            else:
                col_name = self._attrs
                type_flag = '.'
        keys = self.fetch(['Component type'], [type_flag], 2, keys, dic)
        keys = self.fetch(attrs, values, method,keys, dic)
        self.show(keys, dic, col_name)
        return
    
    
    def decode_mlcc(self, rr):
        value = '';
        size = '';
        ctype = '';
        cchar = '';
        tolerance = '';
        tmp = []
        index = 0;
        #get value
        while index < rr.__len__():
            if not rr[index].isdigit():
                index += 1;
                continue;
            while rr[index] != 'V':
                tmp.append(rr[index]);
                index += 1;
            break;
        tmp.append('V');
        value = "".join(tmp);
        
        if rr.find('MLCC') != -1:
            ctype = 'MLCC';
            #get size
            ss = ['0201', '0402', '0603', '0805', '1206']
            for s in ss:
                if rr.find(s) != -1:
                    size = s;
                    break;
        elif rr.find('CAP') != -1:
            ctype = 'CAP PL';
            sscap = ['6.3*8', '6.3*10.5'];
            for s in sscap:
                if rr.find(s) != -1:
                    size = s;
                    break;
        elif rr.find('POSCAP') != -1:
            ctype = 'POSCAP';
            sspos = ['7343/D'];
            for s in sspos:
                if rr.find(s) != -1:
                    size = s;
                    break;

        elif rr.find('PL') != -1:
            ctype = 'PL EL';
            sscap = ['7343/D'];
            for s in sscap:
                if rr.find(s) != -1:
                    size = s;
                    break;
        else:
            print('decode cap wrong!');

        #get x5r, x7r
        cclist = ['Y5V', 'NPO', 'X5R', 'X7R'];
        for cc in cclist:
            if rr.find(cc) != -1:
                cchar = cc;
                break;
            
        #get tolerance
        tol = ['10%', '20%', '5%']
        for toll in tol:
            if rr.find(toll) != -1:
                tolerance = toll;
                break;

        tmp.clear();
        tmp.append(value);
        tmp.append(size);
        tmp.append(ctype);
        tmp.append(cchar);
        tmp.append(tolerance);
        return tmp;
    def decode_res(self, rr):
        value = '';
        size = '';
        tolerance = '';
        tmp = []
        index = 0;
        #get value
        while index < rr.__len__():
            if not rr[index].isdigit():
                index += 1;
                continue;
            while rr[index] != ' ':
                tmp.append(rr[index]);
                index += 1;
            break;
        value = "".join(tmp);
        #get size
        ss = ['0201', '0402', '0603', '0805', '1206']
        for s in ss:
            if rr.find(s) != -1:
                size = s;
                break;
            
        #get tolerance
        tol = ['1%', '3%', '5%', 'JUMP']
        for toll in tol:
            if rr.find(toll) != -1:
                tolerance = toll;
                break;

        tmp.clear();
        tmp.append(value);
        tmp.append(size);
        tmp.append(tolerance);
        return tmp;
test = SCH_db('pre.exp')
#bom = BOM_db('wBOM.txt')
#a = SCH_db('exp.txt')
#b = BOM_db('bom.txt')
#a.parser()
#b.parser()
#breakpoiont
#print('')
