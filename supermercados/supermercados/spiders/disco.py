import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor
from scrapy.loader import itemloaders
#from items import SupermercadosItem
#from scrapy.loader.processors import 

#from configs import CONN_DB
#from sqlalchemy import create_engine
import logging
import pandas
import time

#cot= 'coto.csv'
digitos = ("123456789.,$")
#engine = create_engine(CONN_DB, echo=False)
#logging.info("SE CONECTO COTO ")


utls_reserva = [
    "https://www.disco.com.ar/Almacen/Aceites-y-Vinagres?page=1",
    "https://www.disco.com.ar/Almacen/Aderezos?page=2",
    "https://www.disco.com.ar/Almacen/Arroz-y-Legumbres?page=2",
    "https://www.disco.com.ar/Almacen/Conservas",
    "https://www.disco.com.ar/Almacen/Sal-Pimienta-y-Especias",
    "https://www.disco.com.ar/Almacen/Desayuno-y-Merienda",
    "https://www.disco.com.ar/Almacen/Golosinas-y-Chocolates",
    "https://www.disco.com.ar/Almacen/Harinas",
    "https://www.disco.com.ar/Almacen/Panificados",
    "https://www.disco.com.ar/Almacen/Caldos-Sopas-Pure-y-Bolsas-para-Horno",
    "https://www.disco.com.ar/Almacen/Para-Preparar",
    "https://www.disco.com.ar/Almacen/Pastas-Secas-y-Salsas",
    "https://www.disco.com.ar/Almacen/Snacks",
    "https://www.disco.com.ar/Bebidas/Aguas",
    "https://www.disco.com.ar/Bebidas/A-Base-de-Hierbas",
    "https://www.disco.com.ar/Bebidas/Aperitivos",
    "https://www.disco.com.ar/Bebidas/Bebidas-Blancas",
    "https://www.disco.com.ar/Bebidas/Cervezas",
    "https://www.disco.com.ar/Bebidas/Champagnes",
    "https://www.disco.com.ar/Bebidas/Energizantes",
    "https://www.disco.com.ar/Bebidas/Gaseosas",
    "https://www.disco.com.ar/Bebidas/Generosos",
    "https://www.disco.com.ar/Bebidas/Hielo",
    "https://www.disco.com.ar/Bebidas/Isotonicas",
    "https://www.disco.com.ar/Bebidas/Jugos",
    "https://www.disco.com.ar/Bebidas/Licores",
    "https://www.disco.com.ar/Bebidas/Sidras",
    "disco.com.ar/Bebidas/Vinos",
    "https://www.disco.com.ar/Bebidas/Whiskys",
    "https://www.disco.com.ar/carnes/carne-vacuna",
    "https://www.disco.com.ar/Carnes/Carne-de-Cerdo",
    "https://www.disco.com.ar/Carnes/Carbon-y-Lena",
    "https://www.disco.com.ar/Carnes/Embutidos",
    "https://www.disco.com.ar/carnes/pollos",
    "https://www.disco.com.ar/Carnes/Menudencias",
    "https://www.disco.com.ar/Frutas-y-Verduras/Frutas",
    "https://www.disco.com.ar/Frutas-y-Verduras/Hierbas-Aromaticas-y-Plantines",
    "https://www.disco.com.ar/Frutas-y-Verduras/Huevos",
    "https://www.disco.com.ar/Frutas-y-Verduras/Legumbres-Granos-y-Semillas",
    "https://www.disco.com.ar/Frutas-y-Verduras/Organicos",
    "https://www.disco.com.ar/Frutas-y-Verduras/Verduras",
    "https://www.disco.com.ar/Lacteos/Cremas",
    "https://www.disco.com.ar/Lacteos/Dulce-de-Leche",
    "https://www.disco.com.ar/Lacteos/Leches",
    "https://www.disco.com.ar/Lacteos/Pastas-Frescas-y-Tapas",
    "https://www.disco.com.ar/Lacteos/Mantecas-y-Margarinas",
    "https://www.disco.com.ar/Lacteos/Postres",
    "https://www.disco.com.ar/Lacteos/Yogures",
    "https://www.disco.com.ar/Perfumeria/Cuidado-de-la-Piel",
    "https://www.disco.com.ar/Perfumeria/Cuidado-Capilar",
    "https://www.disco.com.ar/Perfumeria/Cuidado-Personal",
    "https://www.disco.com.ar/Perfumeria/Farmacia",
    "https://www.disco.com.ar/Perfumeria/Cuidado-Oral",
    "https://www.disco.com.ar/bebes-y-ninos/cuidado-del-bebe",
    "https://www.disco.com.ar/Bebes-y-Ninos/Alimentacion",
    "https://www.disco.com.ar/Limpieza/Accesorios-de-Limpieza",
    "https://www.disco.com.ar/Limpieza/Desodorantes-de-Ambiente",
    "https://www.disco.com.ar/Limpieza/Papeles",
    "https://www.disco.com.ar/Limpieza/Calzado",
    "https://www.disco.com.ar/Limpieza/Lavandina",
    "https://www.disco.com.ar/Limpieza/Limpieza-de-Bano",
    "https://www.disco.com.ar/Limpieza/Cuidado-Para-La-Ropa",
    "https://www.disco.com.ar/limpieza/insecticidas",
    "https://www.disco.com.ar/Limpieza/Limpieza-de-Cocina",
    "https://www.disco.com.ar/Limpieza/Limpieza-de-Pisos-y-Muebles",
    "https://www.disco.com.ar/Quesos-y-Fiambres/Quesos",
    "https://www.disco.com.ar/Quesos-y-Fiambres/Fiambres",
    "https://www.disco.com.ar/Quesos-y-Fiambres/Dulces",
    "https://www.disco.com.ar/Quesos-y-Fiambres/Encurtidos-Aceitunas-y-Pickles",
    "https://www.disco.com.ar/Quesos-y-Fiambres/Salchichas",
    "https://www.disco.com.ar/Congelados/Pescados-y-Mariscos",
    "https://www.disco.com.ar/Congelados/Pescados-y-Mariscos",
    "https://www.disco.com.ar/Congelados/Pollo-y-Carnes",
    "https://www.disco.com.ar/Congelados/Vegetales",
    "https://www.disco.com.ar/Congelados/Papas",
    "https://www.disco.com.ar/congelados/helados-y-postres",
    "https://www.disco.com.ar/Congelados/Hamburguesas-y-Milanesas",
    "https://www.disco.com.ar/Congelados/Comidas-Congeladas",
    "https://www.disco.com.ar/Panaderia-y-Reposteria/Panaderia",
    "https://www.disco.com.ar/Panaderia-y-Reposteria/Reposteria",
    "https://www.disco.com.ar/Mascotas/Gatos",
    "https://www.disco.com.ar/Mascotas/Perros",
    "https://www.disco.com.ar/Mascotas/Accesorios-para-Mascotas",
]

