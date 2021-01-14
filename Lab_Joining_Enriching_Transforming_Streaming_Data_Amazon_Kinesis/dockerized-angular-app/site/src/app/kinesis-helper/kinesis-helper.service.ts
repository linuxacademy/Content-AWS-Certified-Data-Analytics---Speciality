import { Injectable } from '@angular/core';
import * as AWS from 'aws-sdk';
import { Observable, Subject } from 'rxjs';
import * as uuid from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class KinesisHelperService {


  constructor() { 
    
  }

  public streamData(region: string, secretAccessKey: string, accessKey: string, streamName: string ): Observable<String>{
    const sendResult = new Subject<String>();
    AWS.config.update({region: region,
      accessKeyId: accessKey,
      secretAccessKey: secretAccessKey});
    const credentials = new AWS.Credentials(AWS.config.credentials);
    const kds = new AWS.Kinesis({ region: region, credentials: credentials });

    const order_id = uuid.v4();
    let order = {};
    let items = [];
    let user_ids = [];
    for(let i = 0; i < Math.floor(Math.random() * 5) + 1; i++){
      items.push(this.grocery_items[Math.floor(Math.random() * this.grocery_items.length) - 1])
    }

    for(let i = 0; i < 500; i++) {
      user_ids.push('uid_'+i);
    }

    let user_id = user_ids[Math.floor(Math.random() * (user_ids.length - 1))]

    
    order["items"] = items;
    order["order_id"] = order_id;
    order["total_cost"] = ((Math.random() * 199.99) + 1.00).toFixed(2)
    order["user_id"] = user_id;

    var payload = JSON.stringify(order);

    var params = {
      Data: payload,
      PartitionKey: order_id,
      StreamName: streamName,
    };
    console.log(payload);

    kds.putRecord(params, function(err, data) {
      if (err) {
        sendResult.error(err);
      }else {
        sendResult.next(payload);
      }
    });
      return sendResult.asObservable(); 
  }

  private grocery_items = ['tropical fruit', 'whole milk', 'pip fruit', 'other vegetables',
  'rolls/buns', 'pot plants', 'citrus fruit', 'beef', 'frankfurter',
  'chicken', 'butter', 'fruit/vegetable juice',
  'packaged fruit/vegetables', 'chocolate', 'specialty bar',
  'butter milk', 'bottled water', 'yogurt', 'sausage', 'brown bread',
  'hamburger meat', 'root vegetables', 'pork', 'pastry',
  'canned beer', 'berries', 'coffee', 'misc. beverages', 'ham',
  'turkey', 'curd cheese', 'red/blush wine',
  'frozen potato products', 'flour', 'sugar', 'frozen meals',
  'herbs', 'soda', 'detergent', 'grapes', 'processed cheese', 'fish',
  'sparkling wine', 'newspapers', 'curd', 'pasta', 'popcorn',
  'finished products', 'beverages', 'bottled beer', 'dessert',
  'dog food', 'specialty chocolate', 'condensed milk', 'cleaner',
  'white wine', 'meat', 'ice cream', 'hard cheese', 'cream cheese ',
  'liquor', 'pickled vegetables', 'liquor (appetizer)', 'UHT-milk',
  'candy', 'onions', 'hair spray', 'photo/film', 'domestic eggs',
  'margarine', 'shopping bags', 'salt', 'oil', 'whipped/sour cream',
  'frozen vegetables', 'sliced cheese', 'dish cleaner',
  'baking powder', 'specialty cheese', 'salty snack',
  'Instant food products', 'pet care', 'white bread',
  'female sanitary products', 'cling film/bags', 'soap',
  'frozen chicken', 'house keeping products', 'spread cheese',
  'decalcifier', 'frozen dessert', 'vinegar', 'nuts/prunes',
  'potato products', 'frozen fish', 'hygiene articles',
  'artif. sweetener', 'light bulbs', 'canned vegetables',
  'chewing gum', 'canned fish', 'cookware', 'semi-finished bread',
  'cat food', 'bathroom cleaner', 'prosecco', 'liver loaf',
  'zwieback', 'canned fruit', 'frozen fruits', 'brandy',
  'baby cosmetics', 'spices', 'napkins', 'waffles', 'sauces', 'rum',
  'chocolate marshmallow', 'long life bakery product', 'bags',
  'sweet spreads', 'soups', 'mustard', 'specialty fat',
  'instant coffee', 'snack products', 'organic sausage',
  'soft cheese', 'mayonnaise', 'dental care', 'roll products ',
  'kitchen towels', 'flower soil/fertilizer', 'cereals',
  'meat spreads', 'dishes', 'male cosmetics', 'candles', 'whisky',
  'tidbits', 'cooking chocolate', 'seasonal products', 'liqueur',
  'abrasive cleaner', 'syrup', 'ketchup', 'cream', 'skin care',
  'rubbing alcohol', 'nut snack', 'cocoa drinks', 'softener',
  'organic products', 'cake bar', 'honey', 'jam', 'kitchen utensil',
  'flower (seeds)', 'rice', 'tea', 'salad dressing',
  'specialty vegetables', 'pudding powder', 'ready soups',
  'make up remover', 'toilet cleaner', 'preservation products'];
}
