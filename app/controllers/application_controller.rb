class ApplicationController < Sinatra::Base
  set :root, File.dirname(__FILE__)

  set :environment, ENV['RACK_ENV']

  set :logging, true

  set :logging, ENV['LOG_LEVEL'] || Logger::DEBUG

  set :http_allow_methods, [
    'POST',
    'GET',
    'OPTIONS',
    'PUT',
    'DELETE'
  ]

  set :http_allow_headers, [
    'Origin',
    'Content-Type',
    'Accept',
    'Authorization',
    'X-Requested-With'
  ]

  set :http_allow_origin, [
    '*'
  ]

  error Etcd::NotDir do
    halt 404, { errors: { message: 'Not found.' }}.to_json
  end

  error Etcd::KeyNotFound do
    exception = Tendrl::HttpResponseErrorHandler.new(env['sinatra.error'])
    halt exception.status, exception.body.to_json
  end

  error JSON::ParserError do
    exception = Tendrl::HttpResponseErrorHandler.new(
      env['sinatra.error'],
      cause: 'invalid_json'
    )
    halt exception.status, exception.body.to_json
  end

  error Errno::ETIMEDOUT do
    exception = Tendrl::HttpResponseErrorHandler.new(
      env['sinatra.error'],
      cause: 'etcd_timeout'
    )
    halt exception.status, exception.body.to_json
  end
  
  error Errno::ECONNREFUSED do
    exception = Tendrl::HttpResponseErrorHandler.new(
      env['sinatra.error'],
      cause: 'etcd_not_reachable'
    )
    halt exception.status, exception.body.to_json
  end

  error do
    exception = Tendrl::HttpResponseErrorHandler.new(
      env['sinatra.error'],
      cause: 'uncaught_exception'
    )
    halt exception.status, exception.body.to_json
  end


  before do
    content_type :json
    response.headers["Access-Control-Allow-Origin"] = 
      settings.http_allow_origin.join(',')
    response.headers["Access-Control-Allow-Methods"] = 
      settings.http_allow_methods.join(',')
    response.headers["Access-Control-Allow-Headers"] = 
      settings.http_allow_headers.join(',')
  end

  options '*' do
    status 200
  end

  protected

  def access_token
    token = nil
    if request.env['HTTP_AUTHORIZATION']
      token = request.env['HTTP_AUTHORIZATION'].split('Bearer ')[-1]
    end
    token
  end

  def etcd
    Tendrl.etcd
  end

end
