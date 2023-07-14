pass_object={
  "formatVersion" : 1,
  "passTypeIdentifier" : "pass.com.pepephone.eventTicket",
  "serialNumber" : "123567881011",
  "webServiceURL" : "https://pepephone.jumpingcrab.com:5000/",
  "authenticationToken" : "k8US4TNekA6E9wHhltFipZcz2wXX30lH2",
  "teamIdentifier" : "SUYF554X6Z",
  "locations" : [
    {
      "longitude" : -122.3748889,
      "latitude" : 37.6189722
    },
    {
      "longitude" : -122.03118,
      "latitude" : 37.33182
    }
  ],
  "barcode" : {
    "message" : "https://www.pepephone.com/",
    "format" : "PKBarcodeFormatPDF417",
    "messageEncoding" : "iso-8859-1"
  },
  "organizationName" : "PepePhone",
  "description" : "Contrato",
  "logoText" : "PepePhone",
  "foregroundColor" : "rgb(0,0,0)",
  "backgroundColor2" : "rgb(6, 222, 241)",
  "backgroundColor" : "rgb(153, 0, 0)",
  "labelColor" : "rgb(255, 255, 255)",
  "stripColor": "rgb(0,0,0)",
  "eventTicket" : {
    "headerFields" : [
      {
        "key" : "titular",
        "label":"TITULAR",
        "value" : "Samuel"
      }
    ],
    "secondaryFields" : [
      {
        "key" : "mes",
        "label" : "MES",
        "value" : "Junio"
      },      
      {
        "key" : "fibra",
        "label" : "Fibra",
        "value" : "300mb",
        "textAlignment" : "PKTextAlignmentCenter"
      },
      {
        "key" : "gigas",
        "label" : "GBs",
        "value" : "45"
      }
    ],
    "auxiliaryFields" : [
      {
        "key" : "facturacion",
        "label" : "FACTURACION",
        "value" : "49€"
      },
      {
        "key" : "firstLine",
        "label" : "Linea principal",
        "value" : "666555777",
        "textAlignment" : "PKTextAlignmentCenter"
      },
      {
        "key" : "secondLine",
        "label" : "Linea secundaria",
        "value" : "666555777",
        "textAlignment" : "PKTextAlignmentCenter"
      }
    ],
    "backFields" : [
      {
        "key" : "website",
        "label" : "Visita nuestra web",
        "value" : "https://www.pepephone.com/"
      },
      {
        "numberStyle" : "PKNumberStyleSpellOut",
        "label" : "Numero de lineas contratadas",
        "key" : "numberStyle",
        "value" : 4
      },
      {
        "label" : "Facturacion del mes actual",
        "key" : "currency",
        "value" : 52,
        "currencyCode" : "EUR"
      },
      {
        "dateStyle" : "PKDateStyleFull",
        "label" : "full date",
        "key" : "dateFull",
        "value" : "1980-05-07T10:00-05:00"
      },
      {
        "label" : "full time",
        "key" : "timeFull",
        "value" : "1980-05-07T10:00-05:00",
        "timeStyle" : "PKDateStyleFull"
      },
      {
        "dateStyle" : "PKDateStyleShort",
        "label" : "short date and time",
        "key" : "dateTime",
        "value" : "1980-05-07T10:00-05:00",
        "timeStyle" : "PKDateStyleShort"
      },
      {
        "dateStyle" : "PKDateStyleShort",
        "label" : "relative date",
        "key" : "relStyle",
        "value" : "2013-04-24T10:00-05:00",
        "isRelative" : True
      }
    ]
  }
}
