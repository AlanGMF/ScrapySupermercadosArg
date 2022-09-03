import scrapy
from scrapy.crawler import CrawlerProcess
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor
#from scrapy.loader import itemloaders
#from items import SupermercadosItem
#from scrapy.loader.processors import 

import logging
import pandas
import time

digitos = ("123456789.,$")

utls_reserva = [
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol/_/N-j9f2pv",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-con-alcohol/_/N-4hulsc",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-infusiones/_/N-dw58vw",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-salsas-y-pur%C3%A9-de-tomate/_/N-os1anu",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-panaderia/_/N-s3bf1a",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-conservas/_/N-1t4efca",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-aceites-y-condimentos/_/N-18r69ct",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-alimento-de-beb%C3%A9s-y-ni%C3%B1os/_/N-nnh9fj",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-encurtidos/_/N-12rkdi1",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-cereales/_/N-ukd5id",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-endulzantes/_/N-1rtbab6",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-harinas/_/N-842qrm",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-arroz-y-legumbres/_/N-c0x2yz",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-especias/_/N-1t0tm80",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-mermeladas-y-dulces/_/N-mj4aa8",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-aderezos-y-salsas/_/N-rv0frc",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-l%C3%A1cteos/_/N-1d443r9",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-pastas-frescas-y-tapas/_/N-1e4im7l",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-fiambres/_/N-1j6o93y",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-comidas-elaboradas/_/N-l535ea",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-quesos/_/N-1d0721n",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-frutas-y-verduras/_/N-zxw18u",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-pescaderia/_/N-yxu4b7",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-carniceria/_/N-176whnp",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-aves/_/N-6drhk5",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos-huevos/_/N-mtdtw6",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-helados-y-postres/_/N-cor40m",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-frutas-congeladas/_/N-14w51iy",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-comidas-congeladas/_/N-m17c6b",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-nuggets-patitas-y-bocaditos/_/N-uh4qr",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-pescaderia/_/N-wgo47s",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-hamburguesas-y-milanesas/_/N-15wfcx5",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-vegetales-congelados/_/N-8efwh3",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-congelados-papas-congeladas-fritas/_/N-1vcscvz",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-lavado/_/N-t2y8zd",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-desodorantes-de-ambiente/_/N-1annh67",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-limpieza-de-ba%C3%B1o/_/N-pz78zm",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-papeles/_/N-ff27jr",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-insecticidas/_/N-6bv3h3",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-limpieza-de-cocina/_/N-1lonain",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-limpieza-de-pisos-y-superficies/_/N-bf8h0x",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-calzado/_/N-1ap445v",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-accesorios-de-limpieza/_/N-ohywgy",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-limpieza-lavandinas/_/N-1ogrrlx",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cuidado-del-cabello/_/N-1w8xczk",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cuidado-bucal/_/N-iak9sv",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cuidado-del-beb%C3%A9-y-la-mam%C3%A1/_/N-1c9xpsw",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-higiene-personal/_/N-721a4h",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-protecci%C3%B3n-femenina/_/N-1csoql4",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-farmacia/_/N-hooak",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-colonias-y-perfumes/_/N-6hnf6f",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cremas-de-belleza/_/N-jpga0a",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-desodorantes-y-antitranspirantes/_/N-2f9qa1",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-pa%C3%B1ales-y-productos-para-incontinencia/_/N-1a8xcmp",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cuidado-de-la-piel/_/N-7d4hhu",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cosm%C3%A9ticos/_/N-85l8um",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-accesorios/_/N-14mninw",
    "https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-perfumer%C3%ADa-cuidado-personal/_/N-sstxyh",
]




class Coto(scrapy.Spider):
    indice = 0
    name = 'coto'
    num_pag = 2

    start_urls = [
        utls_reserva[indice],
    ]

    def parse(self, response):

        url_base = "https://www.cotodigital3.com.ar"
        
        # Selectores
        
        # Trae 96 elementos del response porque trae un <br> y el precio
        precios_productos = response.xpath(
            '//div[contains(@class,"rightList")]/div[contains(@id,"divProductAdd")]/span[@class="atg_store_productPrice" and contains(@style,"display")]/span[@class="atg_store_newPrice"]/text()').getall()
        
        # Trae 48 nombres de elementos
        nombres_productos =  response.xpath(
            '//span[@class="span_productName"]//div//div[@class="descrip_full"]/text()').getall()

        print(f"scraper tiene q buscar la num_pag  {self.num_pag} --------------")
        siguiente_pagina =  response.xpath(
            f'//div[@class="atg_store_pagination"]//ul[@id="atg_store_pagination"]//li//a[contains(@title,"Ir a página {self.num_pag}")]/@href').get()
       
        #Extrae categoria
        url = response.url  
        pos = url.find("catalogo")
        categoria = url[pos:]
        pos = categoria.find("/")
        categoria = categoria[:pos]

        # Se extrae solo el precio del string encontrado
        nuevo_precio=''
        precios_limpios=[]

        for string in precios_productos:

            for digito in string:
                if digito in  digitos:
                    nuevo_precio += digito
            if nuevo_precio != "":
                precios_limpios.append(nuevo_precio)
            nuevo_precio = ''

        for pos, value in enumerate(nombres_productos):
            
            yield {
                "nombre" : nombres_productos[pos],
                "precio" : precios_limpios[pos],
                "categoria" : categoria
            }

        print("")
        print(f"------CATEGORIA-----> {categoria}")
        print("")
        print(f"------PAGINA N°-----> {self.num_pag -1}")
        print("")
        print(f"------PAGINA Actual-----> {self.num_pag}")
        print("")
        
        if siguiente_pagina != None:
            self.num_pag += 1
            print("")
            print(f"------SIGUIENTE PAGINA-----> {siguiente_pagina}")
            print("")
            
            p = url_base + siguiente_pagina
            time.sleep(3) #se espera unos segundos para evitar el baneo de ip departe del servidor
            yield response.follow(p ,callback=self.parse)
        else:
            self.indice += 1
            self.num_pag = 2
            print("entro al ELSE ")
            if  self.indice <= len(utls_reserva)-1:

                next = utls_reserva[self.indice]
                print("")
                print(" ______________________________________")
                print("|se termino de scrapiar el link actual |")
                print("|______________________________________|")
                print("")
                yield response.follow(next ,callback=self.parse)
            else:
                print("--------------------------TERMINO TODO EXITOSAMENTE -----------------------")

if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(Coto)
    procesar.start()