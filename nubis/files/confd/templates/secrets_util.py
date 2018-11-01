config = {
  'proxies'             : {"https" : "http://proxy.service.consul:3128"},
  'MozGeo': {
    'google_api_key' : '{{ getv "/config/Util/MozGeo/GoogleAPIKey" "mozgeo-google-api-key-not-set" }}',
  }
}
