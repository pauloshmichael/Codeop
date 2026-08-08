'use strict';

// EXERCISE 1: VAT Function with Default Parameter



const vatArrow = (amount, rate = 0.15) => amount * rate;

console.log('VAT on 100 ETB (15%):', vatArrow(100)); // 15


// EXERCISE 2: makeCounter Closure

function makeCounter() {
  let count = 0; 
  
  return function() {
    count++;
    return count;
  };
}
/*the scope of the variable count is limited to the makeCounter function. 
It is not accessible from outside, which is why it remains private and cannot be modified directly.
*/

const counter1 = makeCounter();
console.log('Counter 1:', counter1()); 
console.log('Counter 1:', counter1()); 
console.log('Counter 1:', counter1());



// EXERCISE 3: discountBy Factory


function discountBy(rate) {
  return function(price) {
    return price - (price * rate);
  };
}
const memberPrice = discountBy(0.10); 
const salePrice = discountBy(0.30);   

const price = 1000;
console.log(`Original Price: ${price} ETB`);
console.log(`Member Price (10% off): ${memberPrice(price)} ETB`);
console.log(`Sale Price (30% off): ${salePrice(price)} ETB`);
console.log();

// EXERCISE 4: applyToAll Higher-Order Function


function applyToAll(list, fn) {
  const results = [];
  for (let i = 0; i < list.length; i++) {
    results.push(fn(list[i]));
  }
  return results;
}

const prices = [100, 200, 300, 400, 500];
console.log('Original prices:', prices);

const vatRate = 0.15;
const pricesWithVAT = applyToAll(prices, function(price) {
  return price + (price * vatRate);
});

console.log('Prices with VAT (15%):', pricesWithVAT);

const pricesWithVATArrow = applyToAll(prices, (price) => price + (price * 0.15));
console.log('Prices with VAT (arrow):', pricesWithVATArrow);

const discountedPrices = applyToAll(prices, (price) => price * 0.90);
console.log('Prices with 10% discount:', discountedPrices);
console.log();

// EXERCISE 5: forEach with Ethiopian Cities


const ethiopianCities = ['Addis Ababa', 'Dire Dawa', 'Adama', 'Gondar', 'Bahir Dar'];

ethiopianCities.forEach(function(city, index) {
  console.log(`${index + 1}. ${city}`);
});

console.log('\nUsing arrow function:');
ethiopianCities.forEach((city, index) => console.log(`${index + 1}. ${city}`));

console.log('\nFormatted list:');
const cityList = [];
ethiopianCities.forEach((city, index) => {
  cityList.push(`${index + 1}. ${city}`);
});
console.log(cityList.join('\n'));
console.log();
