var AWS = require('aws-sdk');
var glue = new AWS.Glue();

exports.handler = async (event, callback, context) => {
    
    // Lets check to see if any jobs are currently running
    var params = {
      JobName: 'new-job',
    };
    return glue.getJobRuns(params).promise().then((data) => {
      var isJobRunning = false;
      var noJobs = false;
      if(data["JobRuns"].length === 0) {
        noJobs = true;
      }
      console.log(noJobs)
      data["JobRuns"].forEach(job => {
        
        if(job["JobRunState"] !== 'SUCCEEDED') {
          isJobRunning = true;
        }
      });

      if(!isJobRunning || noJobs) {
          var params = {
            JobName: 'new-job',
          };
          console.log('Starting a new job....');
          return glue.startJobRun(params).promise();
      } else {
        return console.log('Not starting a new job...');
      }
        
        
    });
};
