#!/usr/bin/env node
import express from 'express';
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const fs = require('fs')
const amqp =  require ('amqplib/callback_api');
const path = './MOCK_DATA.json';
const queue = 'test_queue';
    amqp.connect(process.env.URL_NAME, (error0, connection) => {
        if (error0) {
            throw error0
        }

        connection.createChannel((error1, channel) => {
            if (error1) {
                throw error1
            }
            

            channel.assertQueue(queue, {durable: false})
            const app = express()
            app.use(express.json())
            channel.consume(queue, async (msg) => {
                fs.appendFile(path,  `${msg.content.toString()} \n`, function (err) {
                    if (err) return console.log(err);
                    /*fs.readFile(path, 'utf8', function(err, data){
                        if (err) return console.log(err);
                        // Display the file content
                        console.log('..',data);
                    });*/
                  });
                
            }, {noAck: true})

            console.log('Listening to port: 8001')
            app.listen(8080)
        })
    })


