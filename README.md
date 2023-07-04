# airflow_WorldBank
(cambiar la api,y realizar el esquema)


## ✨ Elementos del Proceso
- [Instalación y Configuración de Airflow con Docker](#Instalación)
- [DataFrame](#DataFrame)
- [Data Lake](#Data-Lake)
- [Análisis Exploratorio de los Datos](#EDA)
- [Transformación](#Transformación)
- [Data Warehouse](#Data-Warehouse)
- [Análisis](#Análisis)
<br>
<br>
<br>
<br>

<div id='Instalación'/>

### Instalación y Configuración de Airflow con Docker 
En este proyecto se utilizarón diferentes tecnologías, por lo que es necesario la instalación y modificación en algunas de ellas.

1. Instalamos Docker para Windows
   https://docs.docker.com/desktop/install/windows-install/
 
3. Airflow con Docker
Abrimos una terminal de Visual Studio Code

```
# Se crea la carpeta que albergara el proyecto
mkdir airdock
cd airdock

# Clonamos el archivo con la configuración de los contenedores 
Invoke-WebRequest -Uri 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml' -OutFile 'docker-compose.yaml'

# Revisamos que existe el archivo
ls

# Se crean las carpetas que se utilizarán
mkdir .\dags, .\logs, .\plugins, .\temp

# Se crea un archivo con credenciales del enviroment
echo "AIRFLOW_UID=5000" >> .env
echo "AIRFLOW_GID=0" >> .env
```


Hacemos unos cambios en el archivo de yaml:

Para evitar que se carguen dags de ejemplos: 
<p align=center><img width="50%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/yaml1.png"></p><br>

Dar de alta a la carpeta temp
<p align=center><img width="50%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/yaml2.png"></p><br>

Encontrar el puerto para la conexion con dbeaver
<p align=center><img width="40%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/yaml3.png"></p><br>

Cambiar el puerto del airflow 
<p align=center><img width="70%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/yaml4.png"></p><br>


Para inicializar airflow
```
# Corremos docker e inicializamos Airflow
docker-compose-up airflow-init

# si queremos eliminar los contenedores
docker-compose down
```

Si se obtiene un error parecido, abrir el .env en notepad y guardarlo como utf-8
<p align=center><img width="50%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/yaml5.png"></p><br>

En el navegador se coloca localhosto:8088
<p align=center><img width="50%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/web1.png"></p><br>

Una vez en el formulario, se coloca airflow en usuario y en contraseña

<p align=center><img width="80%" src= "https://github.com/hikikae/airflow_WorldBank/blob/main/src/web2.png"></p><br>

<br>

<div id='DataFrame'/>

### DataFrame 
El resultado de la consulta de la API se guarda en un dataframe, gracias a la librería de pandas.
```
def convert_to_dataframe(data):
    df = pd.DataFrame(data)
```

<br>

<div id='Data-Lake'/>

### Data Lake
Los datos podemos colocarlos en un repositorio ya sea con un vendor (GCP, Azure, AWS) pero en este punto se puede considerar como un data lake ya que se encuentran en su formato original.  

```
 df = df.to_json('./raw_data.json')
```

<br>

<div id='EDA'/>

### <a href="https://github.com/hikikae/Pipeline_World_Bank/blob/main/EDAWorldBank.ipynb"> Análisis Exploratorio de los Datos </a>
Tenemos que entender que significan nuestros datos, para ello se realiza un EDA y así tomar decisiones de que datos podrían servir en futuros pasos del análisis.
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 16492 entries, 0 to 16491
Data columns (total 10 columns):
 #   Column           Non-Null Count  Dtype  
---  ------           --------------  -----  
 0   indicator.id     16492 non-null  object 
 1   indicator.value  16492 non-null  object 
 2   country.id       16492 non-null  object 
 3   country.value    16492 non-null  object 
 4   countryiso3code  16492 non-null  object 
 5   date             16492 non-null  int64  
 6   value            16400 non-null  float64
 7   unit             16492 non-null  object 
 8   obs_status       16492 non-null  object 
 9   decimal          16492 non-null  int64  
dtypes: float64(1), int64(2), object(7)
memory usage: 1.3+ MB
```
<br>

Los pasos básicos de un EDA
1. Revisión duplicados
2. Revisión y manejo de campos nulos
3. Revisión de Outliers

<br>


<div id='Transformación'/>

### Transformación
Nuestros datos contienen algunos campos que están anidados, es decir, el formato json es un objeto dentro de este objeto hay nuevos objetos o arrays, que permiten hacer más legible los datos, pero no para nosotros que nos encargamos de analizarlos, por lo que uno de los pasos necesarios es eliminar esa anidación.
```
   df = pd.read_json('./raw_data.json')    
    #flat json
    df= pd.concat([pd.json_normalize(df['indicator']).add_prefix('indicator.'),
                     pd.json_normalize(df['country']).add_prefix('country.'),
                     df.drop(['indicator', 'country'], axis=1)], axis=1)  
```

<br>

<div id='Data-Warehouse'/>

### Data Warehouse
Cuando se tienen ya normalizados, y ya seleccionando los datos que sirven para el giro del negocio se pueden considerar "limpios" y estos datos podrían estar como el data lake en un repositorio de un vendor, y a este se le conoce como un data wearhouse.

```
    #this could be the datawarehouse
    df.to_csv('./clean_data.csv', index=False)
```

<br>

<div id='Análisis'/>

### Análisis
El análisis de los datos se realizaron en varias etapas: EDA, durante el Pipeline y mediante un tablero de <a href="https://github.com/hikikae/Pipeline_World_Bank/blob/main/worldbank.pbix"> PowerBI </a>. 

Tablero
<br>
<p align=center><img width="80%" src= "https://github.com/hikikae/Pipeline_World_Bank/blob/main/src/tablero.png"></p><br>
<br>

Otras gráficas

<br>
<p align=center><img width="80%" src= "https://github.com/hikikae/Pipeline_World_Bank/blob/main/src/growth_percentage.png"></p><br>

<p align=center><img width="80%" src= "https://github.com/hikikae/Pipeline_World_Bank/blob/main/src/proyeccion_India_China.png"></p><br>
<br>

##  🛠️ Tecnologías 
- Google Colab
- WorldBank API
- Pandas
- Python
- Numpy
- Sklearn

## Agradecimiento y Contacto
Gracias por interesarte en mi proyecto y si tienes alguna duda no dudes en contactarte conmigo.

Angélica García Díaz ---- <a href="https://www.linkedin.com/in/angelica-garc%C3%ADa-diaz/">LinkedIn </a>, mail:  angelicagarciad@gmail.com <br>

 😇
