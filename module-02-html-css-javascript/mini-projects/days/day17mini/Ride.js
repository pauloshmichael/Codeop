'use strict';

//  PART  1    FUNCTION BASICS (ARROWS, DEFAULT , REST )
const sumDistances = (...distances) => {
  let totalDistance = 0;
  for (const distance of distances) {
    totalDistance += distance;
  }
  return totalDistance;
};

console.log(sumDistances(10, 20, 25, 50)); 


const calculateBaseFare = (totalDistance, ratePerKm = 15) => {
  return totalDistance * ratePerKm;
};

const formatCurrency = (amount) => {
  return amount.toFixed(2) + " ETB";
};
console.log(formatCurrency(120.501));

// PART 2: HIGHER-ORDER FUNCTIONS
function makeSurgeMultiplier(surgeRate) {
  return function(baseFare) {
    return baseFare * surgeRate;
  };
}
let double = makeSurgeMultiplier(1.5);
console.log(double(100)); 


// PART 3: CLOSURES

function makeDriverTracker() {
  let tripsCompleted = 0;
  
  return {
    recordTrip() {
      tripsCompleted++;
      return tripsCompleted;
    },
    getTrips() {
      return tripsCompleted;
    }
  };
}
let driver1 = makeDriverTracker();
driver1.recordTrip();
driver1.recordTrip();
driver1.recordTrip();
driver1.recordTrip();
console.log(driver1.getTrips());

// PART 4: PUTTING IT ALL TOGETHER
function generateReceipt(distances, surgeFn, tracker, callback) {

  const tripNumber = tracker.recordTrip();
  

  const totalDistance = sumDistances(...distances);
  

  const baseFare = calculateBaseFare(totalDistance);
  

  const totalFare = surgeFn(baseFare);
  

  const formattedFare = formatCurrency(totalFare);
  
  
  const message = `Trip #${tripNumber}: Total Fare is ${formattedFare}.`;
  
 
  callback(message);
}


const tayesTracker = makeDriverTracker();
const standardPricing = makeSurgeMultiplier(1.0);
const rushHourPricing = makeSurgeMultiplier(1.5);


const printToConsole = (message) => console.log(message);


generateReceipt([2, 3], standardPricing, tayesTracker, printToConsole);
// Expected Output: "Trip #1: Total Fare is 75.00 ETB."


generateReceipt([10], rushHourPricing, tayesTracker, printToConsole);
// Expected Output: "Trip #2: Total Fare is 225.00 ETB."