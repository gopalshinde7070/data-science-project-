from flask import Flask,render_template,request

import pickle 
app=Flask(__name__)

with open('customer_conversion.pkl','rb') as f:
    model=pickle.load(f)

@app.route('/')

def home():
    return render_template('index.html')
@app.route('/predict',methods=['POST'])

def predict():
    Gender=int(request.form['Gender'])
    TimeSpent_minutes=int(request.form['TimeSpent_minutes'])
    PagesViewed=int(request.form['PagesViewed'])
    EmailSent=int(request.form['EmailSent'])
    FormSubmissions=int(request.form['FormSubmissions'])
    ResponseTime_hours=int(request.form['ResponseTime_hours'])
    FollowUpEmails=int(request.form['FollowUpEmails'])

    def LeadSource(LeadSourceclass):
        if LeadSourceclass=='Email':
            LeadSource_Email=1
            LeadSource_Organic=0
            LeadSource_Referral=0
            LeadSource_Social_Media=0



        elif LeadSourceclass=='Organic':
            LeadSource_Email=0
            LeadSource_Organic=1
            LeadSource_Referral=0
            LeadSource_Social_Media=0


        elif LeadSourceclass=='Referral':
            LeadSource_Email=0
            LeadSource_Organic=0
            LeadSource_Referral=1
            LeadSource_Social_Media=0

        elif LeadSourceclass=='Social Media':
            LeadSource_Email=0
            LeadSource_Organic=0
            LeadSource_Referral=0
            LeadSource_Social_Media=1
        return LeadSource_Email,LeadSource_Organic,LeadSource_Referral,LeadSource_Social_Media
    LeadSourceclass=(request.form['LeadSource'])
    LeadSource_Email,LeadSource_Organic,LeadSource_Referral,LeadSource_Social_Media=LeadSource(LeadSourceclass)

    def LeadStatus(LeadStatusclass):
        if LeadStatusclass=='Cold':
            LeadStatus_Cold=1
            LeadStatus_Hot=0
            LeadStatus_Warm=0
        elif LeadStatusclass=='Hot':
            LeadStatus_Cold=0
            LeadStatus_Hot=1
            LeadStatus_Warm=0
        elif LeadStatusclass=='Warm':
            LeadStatus_Cold=0
            LeadStatus_Hot=0
            LeadStatus_Warm=1
        return LeadStatus_Cold,LeadStatus_Hot,LeadStatus_Warm
    
    LeadStatusclass=(request.form['LeadStatus'])
    LeadStatus_Cold,LeadStatus_Hot,LeadStatus_Warm=LeadStatus(LeadStatusclass)

    def deviceType(deviceTypeclass):
        if deviceTypeclass=='Desktop':
          DeviceType_Desktop=1
          DeviceType_Mobile=0
          DeviceType_Tablet=0

        elif deviceTypeclass=='Mobile':
          DeviceType_Desktop=0
          DeviceType_Mobile=1
          DeviceType_Tablet=0
        elif deviceTypeclass=='Tablet':
          DeviceType_Desktop=0
          DeviceType_Mobile=0
          DeviceType_Tablet=1
        return DeviceType_Desktop,DeviceType_Mobile,DeviceType_Tablet

    deviceTypeclass=(request.form['DeviceType'])
    DeviceType_Desktop,DeviceType_Mobile,DeviceType_Tablet=deviceType(deviceTypeclass)

    def ReferralSource(ReferralSourceclass):
        if ReferralSourceclass=='Direct':
           ReferralSource_Direct=1
           ReferralSource_Facebook=0
           ReferralSource_Google=0
           ReferralSource_ReferralSite=0
           ReferralSource_Twitter=0

        elif ReferralSourceclass=='Facebook':
           ReferralSource_Direct=0
           ReferralSource_Facebook=1
           ReferralSource_Google=0
           ReferralSource_ReferralSite=0
           ReferralSource_Twitter=0

        elif ReferralSourceclass=='Google':
           ReferralSource_Direct=0
           ReferralSource_Facebook=0
           ReferralSource_Google=1
           ReferralSource_ReferralSite=0
           ReferralSource_Twitter=0

        elif ReferralSourceclass=='ReferralSite':
           ReferralSource_Direct=0
           ReferralSource_Facebook=0
           ReferralSource_Google=0
           ReferralSource_ReferralSite=1
           ReferralSource_Twitter=0

        elif ReferralSourceclass=='Twitter':
           ReferralSource_Direct=0
           ReferralSource_Facebook=0
           ReferralSource_Google=0
           ReferralSource_ReferralSite=0
           ReferralSource_Twitter=1

        return ReferralSource_Direct,ReferralSource_Facebook,ReferralSource_Google,ReferralSource_ReferralSite,ReferralSource_Twitter
    ReferralSourceclass=(request.form['ReferralSource'])
    ReferralSource_Direct,ReferralSource_Facebook,ReferralSource_Google,ReferralSource_ReferralSite,ReferralSource_Twitter=ReferralSource(ReferralSourceclass)


    def PaymentHistory(PaymentHistoryclass):
        if PaymentHistoryclass=='Good':
           PaymentHistory_Good=1
           PaymentHistory_No_Payment=0
        elif PaymentHistoryclass=='No Payment':
           PaymentHistory_Good=0
           PaymentHistory_No_Payment=1

        return PaymentHistory_Good,PaymentHistory_No_Payment

    PaymentHistoryclass=(request.form['PaymentHistory'])

    PaymentHistory_Good,PaymentHistory_No_Payment=PaymentHistory(PaymentHistoryclass)
    
    final=[[Gender,TimeSpent_minutes,PagesViewed,EmailSent,FormSubmissions,ResponseTime_hours,FollowUpEmails,
            LeadSource_Email,LeadSource_Organic,LeadSource_Referral,LeadSource_Social_Media,
            LeadStatus_Cold,LeadStatus_Hot,LeadStatus_Warm,
            DeviceType_Desktop,DeviceType_Mobile,DeviceType_Tablet,
            ReferralSource_Direct,ReferralSource_Facebook,ReferralSource_Google,ReferralSource_ReferralSite,ReferralSource_Twitter,
            PaymentHistory_Good,PaymentHistory_No_Payment]]
    ans=model.predict(final)
    final_ans=int(ans[0])
    if(final_ans==0):
       pred='❌ This lead is unlikely to convert.'
    elif(final_ans==1):
       pred='✅ This lead is likely to convert '
    return render_template('index.html',final_ans_of_prediction=pred)



if __name__=='__main__':
    app.run(debug=True)
