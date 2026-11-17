#!/usr/bin/env ruby

require "csv"

source_path, public_path = ARGV
abort "Usage: sanitize_stringing_log.rb SOURCE PUBLIC" unless source_path && public_path

public_headers = ["Date Completed", "Racket", "String", "Tension", "Paid", "Picked up", "Gender"]
rows = CSV.read(source_path, headers: true, encoding: "bom|utf-8")

CSV.open(public_path, "wb", write_headers: true, headers: public_headers) do |csv|
  rows.each do |row|
    csv << public_headers.map { |header| row[header].to_s }
  end
end
