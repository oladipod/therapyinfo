import pymysql


try:
    con = pymysql.connect(host='167.99.98.149',user='remoteroot',passwd='9ZLkPeH4VZ!!p7t+nyE',port=3306)
    cur = con.cursor()
except Exception as e:
    print(e)



query1 = "CREATE TABLE psychologytoday(therapist_id INT AUTO_INCREMENT, profile_link VARCHAR, profile_photolink VARCHAR, name VARCHAR, title VARCHAR, phone VARCHAR, spec_top VARCHAR, spec_issues VARCHAR, spec_mental VARCHAR, spec_sex VARCHAR, clientfocus_ethnic VARCHAR, clientfocus_speak VARCHAR, clientfocus_faith VARCHAR, clientfocus_age VARCHAR, clientfocus_community VARCHAR, treatapproach_typestherapy VARCHAR, treatapproach_modality VARCHAR, about VARCHAR, fo_cps VARCHAR, fo_slidingscale VARCHAR, fo_payby VARCHAR, fo_insurance VARCHAR, ft_sessionfee VARCHAR, ft_couplefee VARCHAR, ft_payby VARCHAR, qual_practice VARCHAR, qual_school VARCHAR, qual_gradyear VARCHAR, qual_licensestate VARCHAR, qual_licenseprovince VARCHAR, qual_supervisor VARCHAR, qual_supervisorlicense VARCHAR, qual_membership VARCHAR, qual_training VARCHAR, qual_degdiploma VARCHAR, addcred_certificate1 VARCHAR, addcred_certificate2 VARCHAR, addcred_certificate_date1 VARCHAR, addcred_certificate_date2 VARCHAR, addcred_membership VARCHAR, addcred_degdiploma1 VARCHAR, addcred_degdiploma2 VARCHAR,  verification VARCHAR, pro_connect VARCHAR, groups VARCHAR, address1 VARCHAR, address2 VARCHAR, website_url VARCHAR, profile_pix BLOB)"
cur.execute(query1)
con.commit()

# query2 = "INSERT INTO psychologytoday (profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex, clientfocus_ethnic, clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy, treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee, ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor, qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2, verification, pro_connect, groups, address1, address2, website_url, profile_pix)" \
#           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
# args2 = (profile_link, profile_photolink, name, title, phone, spec_top, spec_issues, spec_mental, spec_sex,clientfocus_ethnic, clientfocus_speak, clientfocus_faith, clientfocus_age, clientfocus_community, treatapproach_typestherapy, treatapproach_modality, about, fo_cps, fo_slidingscale, fo_payby, fo_insurance, ft_sessionfee, ft_couplefee, ft_payby, qual_practice, qual_school, qual_gradyear, qual_licensestate, qual_licenseprovince, qual_supervisor, qual_supervisorlicense, qual_membership, qual_training, qual_degdiploma, addcred_certificate1, addcred_certificate2, addcred_certificate_date1, addcred_certificate_date2, addcred_membership, addcred_degdiploma1, addcred_degdiploma2, verification, pro_connect, groups, address1, address2, website_url, profile_pix)
	
# try:
#     conn = pymysql.connect(host='167.99.98.149',user='remoteroot',passwd='9ZLkPeH4VZ!!p7t+nyE',port=3306)
#     cur = conn.cursor()
#     cur.execute(query2, args2)
#     conn.commit()
#     print ("Data saved successfully!")

# except Exception as error:
#     print("Error saving database with error: "+str(error))