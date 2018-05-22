
# coding: utf-8

# In[9]:


from astropy.io import fits
from astropy.table import Table


# In[10]:


file= '/home/harry/Descargas/BAT_catalog.fits'


# In[11]:


hdu_list = fits.open(file)
hdu_list.info()


# In[12]:


file_data = hdu_list[0].data


# #hdu_list.close()

# In[13]:


print(hdu_list[1].columns)


# In[14]:


evt_data = Table(hdu_list[1].data)


# In[15]:


evt_data


# In[17]:


evt_data.info()


# In[19]:


evt_data["NAME"]


# In[20]:


datos = hdu_list[1].data


# In[23]:


names = datos["NAME"]


# In[24]:


names


# In[26]:


datos.field(0)


# - tolist nos pasa el charArray a una lista

# In[28]:


datos_lista=datos.field(0).tolist()


# In[30]:


datos_lista

