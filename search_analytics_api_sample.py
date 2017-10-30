import argparse
import sys
from googleapiclient import sample_tools
from datetime import datetime
import smtplib

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))

def main(argv,properties):
  service, flags = sample_tools.init(argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')
  # First run a query to learn which dates we have data for. You should always
  # check which days in a date range have data before running your main query.
  
  # This query shows data for the entire range, grouped and sorted by day,
  # descending; any days without data will be missing from the results.
  list_of_propery_names = ['India-DCH','Indonesia','Philippines','Diagnostics']
  if properties not in list_of_propery_names:
    
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date']
        # 'dimensionFilterGroups':[{
        #     'filters':[{
        #         'dimension':'country',
        #         'expression':'ind'
        #     }]
        #   }]
    }
    response = execute_request(service, flags.property_uri, request)
    print_table(response, properties)

  elif properties == 'India-DCH':
    request_doctors = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'country',
                'expression':'ind'
            },{
            'dimension':'page',
            'operator':'contains',
            'expression':'/doctor'
            }]
          }]
    }
    response1 = execute_request(service, flags.property_uri, request_doctors)
    request_clinics = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'country',
                'expression':'ind'
            },{
            'dimension':'page',
            'operator':'contains',
            'expression':'/clinic'
            }]
          }]
    }
    response2 = execute_request(service, flags.property_uri, request_clinics)
    intermediate_Respone = add_responses(response1,response2)
    request_hospitals = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'country',
                'expression':'ind'
            },{
            'dimension':'page',
            'operator':'contains',
            'expression':'/hospitals'
            }]
          }]
    }
    response3 = execute_request(service, flags.property_uri, request_hospitals)

    print_table(add_responses(intermediate_Respone,response3), properties)
    # print(response)

  elif properties == 'Philippines':
    flags.property_uri = 'https://www.practo.com/'
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'country',
                'expression':'phl'
            }]
          }]
    }
    response = execute_request(service, flags.property_uri, request)
    print_table(response, properties)

  elif properties=='Indonesia':
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
    }
    response1 = execute_request(service, flags.property_uri, request)
    request_id_id = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
    }
    flags.property_uri = 'https://www.practo.com/indonesia'
    response2 = execute_request(service, flags.property_uri, request_id_id)
    print_table(add_responses(response1,response2), properties)

  elif properties=='Diagnostics':
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date']
    }
    response1 = execute_request(service, flags.property_uri, request)
    request_tests = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'page',
                'operator':'contains',
                'expression':'/test'
              }]
            }]
    }
    flags.property_uri = 'https://www.practo.com/'
    response2 = execute_request(service, flags.property_uri, request_tests)
    intermediate_Respone = add_responses(response1,response2)
    request_diagnostics = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date'],
        'dimensionFilterGroups':[{
            'filters':[{
                'dimension':'page',
                'operator':'contains',
                'expression':'/diagnostic'
              }]
            }]
    }
    flags.property_uri = 'https://www.practo.com/'
    response3 = execute_request(service, flags.property_uri, request_diagnostics)
    print_table(add_responses(intermediate_Respone,response3),properties)

################################################
################# NOT USEFUL ###################
  # print(response)

  # Get totals for the date range.
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, 'Totals')
#################################################
#################### USEFUL #####################
  # Get top 10 queries for the date range, sorted by click count, descending.
  # this should go into the queries DB
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date,
  #     'dimensions': ['query'],
  #     # 'rowLimit': 10
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, properties)
################################################
################# NOT USEFUL ###################
  # # Get top 11-20 mobile queries for the date range, sorted by click count, descending.
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date,
  #     'dimensions': ['query'],
  #     'dimensionFilterGroups': [{
  #         'filters': [{
  #             'dimension': 'device',
  #             'expression': 'mobile'
  #         }]
  #     }],
  #     'rowLimit': 10,
  #     'startRow': 10
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, 'Top 11-20 Mobile Queries')

################################################
################### USEFUL #####################
  # # Get top 10 pages for the date range, sorted by click count, descending.
  # this should go into the page DB
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date,
  #     'dimensions': ['page'],
  #     # 'rowLimit': 10
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, 'Top Pages')

################################################
################# NOT USEFUL ##################
  # # Get the top 10 queries in India, sorted by click count, descending.
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date,
  #     'dimensions': ['query'],
  #     'dimensionFilterGroups': [{
  #         'filters': [{
  #             'dimension': 'country',
  #             'expression': 'ind'
  #         }]
  #     }],
  #     'rowLimit': 10
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, 'Top queries in India')

################################################
################# NOT USEFUL ##################
  # # Group by both country and device.
  # request = {
  #     'startDate': flags.start_date,
  #     'endDate': flags.end_date,
  #     'dimensions': ['country', 'device'],
  #     'rowLimit': 10
  # }
  # response = execute_request(service, flags.property_uri, request)
  # print_table(response, 'Group by country and device')


def execute_request(service, property_uri, request):
  """Executes a searchAnalytics.query request.
  Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.
  Returns:
    An JSON of response rows.
  """
  return service.searchanalytics().query(
      siteUrl=property_uri, body=request).execute()

def two_dec(number):
  '''FORMATS THE UNICODE NUMBER TO A FLOAT NUMBER
  ARGS:
    NUMBER: JUST TAKES A NUMBER
  '''
  return format(number,'.2f')

def print_table(response, title):
  """Prints out a response table.
  Each row contains key(s), clicks, impressions, CTR, and average position.
  Args:
    response: The server response to be printed as a formatted table.
    title: The title of the table.
  """
  print (title + ':')

  if 'rows' not in response:
    print ('Empty response')
    return

  rows = response['rows']
  row_format = '{:<20}' + '{:>20}' * 4
  print (row_format.format('Date', 'Clicks', 'Impressions', 'CTR', 'Position'))
  for row in rows:
    keys = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys'])
    print (row_format.format(
        keys, row['clicks'], row['impressions'], str(two_dec(row['ctr']*100))+"%", two_dec(row['position'])))
    print("\n")


def add_responses(response1,response2):
  final_response = {'rows': [{'keys': ['2017-10-24'], 
  'clicks': 327729.0, 
  'impressions': 3435273.0,
  'ctr': 0.095401151524202,
  'position': 5.375560253872108}],
  'responseAggregationType': 'byProperty'}
  response1_clicks = 0.0
  response1_impressions = 0.0
  response1_ctr = 0.0
  response1_position = 0.0
  response2_clicks = 0.0
  response2_impressions = 0.0
  response2_ctr = 0.0
  response2_position = 0.0

  for row1 in response1['rows']:
    response1_clicks = row1['clicks']
    response1_impressions = row1['impressions']
    response1_ctr = row1['ctr']
    response1_position = row1['position']

  for row2 in response2['rows']:
    response2_clicks = row2['clicks']
    response2_impressions = row2['impressions']
    response2_ctr = row2['ctr']
    response2_position = row2['position']

  final_response['rows'][0]['clicks'] = int(response2_clicks)+int(response1_clicks)
  final_response['rows'][0]['impressions'] = response2_impressions+response1_impressions
  final_response['rows'][0]['ctr'] = response2_ctr+response1_ctr
  final_response['rows'][0]['position'] = (response2_position+response1_position)/2

  return final_response

if __name__ == '__main__':
  # argvs1 = ['search_analytics_api_sample.py', 'https://www.practo.com/pt-br', '2017-09-30']
  name_of_the_code = 'search_analytics_api_sample.py'
  now=datetime.now()
  dict_of_urls = {'Brazil':'https://www.practo.com/pt-br',
  'Indonesia':'https://www.practo.com/id-id/indonesia',
  'Consult':'https://www.practo.com/consult',
  'Diagnostics':'https://www.practo.com/labs',
  'Singapore':'https://www.practo.com/singapore',
  'Philippines':'https://www.practo.com/philippines',
  'India-DCH':'https://www.practo.com/',
  'Practo Blog':'https://blog.practo.com/',
  'Healthfeed':'https://www.practo.com/healthfeed/',
  'Practo pedia':'https://www.practo.com/medicine-info/',
  'Order':'https://www.practo.com/order'}
  for properties in dict_of_urls:
    argvs1=[]
    argvs1.append(name_of_the_code)
    argvs1.append(dict_of_urls[properties])
    argvs1.append(str(now.year)+"-"+str(now.month)+"-"+str(now.day-3))
    argvs1.append(str(now.year)+"-"+str(now.month)+"-"+str(now.day-3))
    main(argvs1,properties)
  server = smtplib.SMTP('smtp.gmail.com',587)
  server.starttls()
  server.login('jarvis.newsteller@gmail.com','jarvis123')
  runtime = datetime.now()-now
  print(runtime)
  server.sendmail('SEO_BOT','deepesh.p@practo.com','the code was run successfully')
  server.quit()














