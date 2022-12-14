# netbox.groups.azuread
A python program for Netbox and assigning group/super user permissions via AzureAD 

AzureAD related customizations for Netbox deployment.


## Usage


- Edit /opt/netbox/netbox/netbox/settings.py and find this section SOCIAL_AUTH_PIPELINE and add to the bottom
```
"eis.netbox.azuread.group_sync",  #This is called from a custom package named "azureAD in gitlab" from group "Infrastructure"
```


- Edit /opt/netbox/netbox/netbox/configuration.py and find the section #Remote Authentication Support
```
#Remove everything under #remote authentication support and add this:
REMOTE_AUTH_ENABLED = True
REMOTE_AUTH_HEADER = 'HTTP_REMOTE_USER'
REMOTE_AUTH_AUTO_CREATE_USER = False
REMOTE_AUTH_BACKEND = 'social_core.backends.azuread.AzureADOAuth2' #Use AzureAD Social_Core Backend
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = '58b399bd-1696-4ccb-8df3-f434e5e41613' #This key is located under App registrations in AzureAD - EIS NetDev - "Application (client) ID"
SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = '<secret here>' #This Secret is located under App registrations in AzureAD -EIS Netdev - "Client Secrets" - "NetDev SSO"
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True #Use UID as the username for Netbox
```
