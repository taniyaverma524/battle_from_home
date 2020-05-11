from config import settings
from libraries.Functions import base64encode
from datetime import datetime ,timedelta

def forgot_pwd_email_content(user, token,base_url ):
    url_encoded_data = base64encode(user)
    time=str(datetime.now()+timedelta(days=1))
    path='http://' + base_url
    # url = path + "http://localhost:4200/forget_password_complete/" + token  + time
    url ="http://localhost:4200/forget_password_complete/" + token +'/'+ time
    content = """\
    <body style="margin: 0;padding: 0;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" >
        <table width="595" border="0" cellspacing="0" cellpadding="0" align="left">
            <tr>
                <td width="10%">&nbsp;</td>
                <td style="font-size:16px;color: #181b14;line-height: 24px;font-family: arial;">
                    <br><br> Hi User <br><br>
                    <span style="line-height:34px;">
                        Email :   <strong>"""+user.email+"""</strong>                                                           
                        <br> 
                        <strong>
                            <a href="""+url+""">Click here</a>
                        </strong> to reset your password.   
                    </span>		
                </td><td width="5%">&nbsp;</td>
            </tr>
        </table>
    </table>
</body>
    """
    return content



