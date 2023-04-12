import csv
from datetime import datetime

#Opening a 'homework.csv' file to read and parse the data

with open('homework.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    keys_list = list(csv_reader.fieldnames)


    #Opening a 'formatted.csv' file to write the formatted data from 'homework.csv' file

    with open('formatted.csv', 'w', newline='', encoding='utf-8') as f_file:
        fieldnames = keys_list

        csv_writer = csv.DictWriter(f_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        csv_file.seek(0)

        for line in csv_reader:

            #Converting date format to ISO 8601.

            if line['system creation date'] == 'system creation date':
                continue
            date_string = line['system creation date']
            date_object = datetime.strptime(date_string, '%m/%d/%y')
            iso_date_string = date_object.isoformat()
            line['system creation date'] = iso_date_string

            #Rounding the currency to cents.

            for el in line.keys():
                if 'price' in el:
                    if '$' in line[el]:
                        clear_el = line[el].replace('$', '')
                        rounded_el = round(float(clear_el), 2)
                        line[el] = rounded_el
                    elif not line[el]:
                        line[el] = '0'
                    else:
                        line[el] = line[el]
                

            #Dimensions without units, assume inches. Converting any units to inches.

            strings_to_check = {'width', 'depth', 'height', 'length', 'diameter', 'dimension', 'dimensions', 'volume', 'extension', 'hcwo'}

            for unit in line.keys():
                for string in strings_to_check:
                    if string in unit:
                        if '(inches)' in unit:
                            line[unit] = line[unit]
                        elif '(cubic feet)' in unit:
                            cubic_feet_str = line[unit]
                            if cubic_feet_str != '':
                                cubic_inches_round = round(float(cubic_feet_str) * 1.728, 2)
                                line[unit] = cubic_inches_round
                            else:
                                pass
                        elif '(feet)' in unit:
                            feet_str = line[unit]
                            if feet_str != '':
                                ft_inches_round = round(float(feet_str) * 12, 2)
                                line[unit] = ft_inches_round
                            else:
                                pass
                        elif 'meters' in unit:
                            meters_str = line[unit]
                            if meters_str != '':
                                m_inches_round = round(float(meters_str) * 39.37, 2)
                                line[unit] = m_inches_round
                            else:
                                pass
                        elif 'centimeters' in unit:
                            cm_str = line[unit]
                            if cm_str != '':
                                cm_inches_round = round(float(cm_str) / 2.54, 2)
                                line[unit] = cm_inches_round
                            else:
                                pass
                        elif 'millimeters' in unit:
                            mm_str = line[unit]
                            if mm_str != '':
                                mm_inches_round = round(float(mm_str) / 25.4, 2)
                                line[unit] = mm_inches_round
                            else:
                                pass

            #Weights without units, assume pounds. Converting anything which isn't in pounds to pounds.
        
            for w in line.keys():
                if 'weight' in w:
                    if 'pound' in w:
                        line[w] = line[w]
                    elif 'kilogram' in w:
                        kg_str = line[w]
                        if kg_str != '':
                            kg_pound_round = round(float(kg_str) * 2.20462, 2)
                            line[w] = kg_pound_round
                        else:
                            pass
                    elif 'gram' in w:
                        g_str = line[w]
                        if g_str != '':
                            g_pound_round = round(float(g_str) * 0.00220462, 2)
                            line[w] = g_pound_round
                        else:
                            pass
                    elif 'ounce' in w:
                        oz_str = line[w]
                        if oz_str != '':
                            oz_pound_round = round(float(oz_str) * 0.0625, 2)
                            line[w] = oz_pound_round
                        else:
                            pass
                    elif 'ton' in w:
                        t_str = line[w]
                        if t_str != '':
                            t_pound_round = round(float(t_str) * 2204.62, 2)
                            line[w] = t_pound_round
                        else:
                            pass

            #UPC / Gtin / EAN handling as strings
            
            strs_to_check = ['UPC', 'Gtin', 'EAN']
            for item in line.keys():
                for elm in strs_to_check:
                    if elm.lower() in item:
                        line[item] = str(line[item])
                    


    
    
            csv_writer.writerow(line)
       