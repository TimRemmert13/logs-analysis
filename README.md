 # Logs Analysis
 A python script that acts as a reporting tool for live insights from a PostgreSQL database and 
 displays results on your local machine in plain text.

 ## Dependencies

 1. Python 3.6.0 or greater
    * You can check your current version of Python by running the command ```Python --version```
    in your local machines terminal.

2. VirtualBox version 5.1
    * newer versions do not work with the current release of vagrant
    * you can download VirtualBox at 
    [virtualbox.org](https://www.virtualbox.org)

3. Vagrant 
    * Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem
    * You can download vagrant at [vagrantup.com](https://vagrantup.com) and install the version for your operating system.

## Getting Started

1. clone the repository at [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)

2. change to this new directory and then change to the vagrant directory.

3. inside the vagrant directory clone this respository or place the opened downloaded zip file of this repository.

4. Open the newsdata.zip file and move the newdata.sql file to the parent vagrant directory. You can achieve this in Mac OS or Linux with the command ```mv newsdata.sql ...```

5. ```cd``` to the vagrant directory and run the command ```vagrant up```. This will download the Linux operating System and install it.

6. Run the command ```vagrant ssh``` to log in to your newly installed Linux VM!

7. To load the data run the command ```psql -d news -f newsdata.sql```

8. To execute the program run the change directories to the log-analysis directory and run the command ```python report.py```

9. You did it! the results of the analysis report will be in the text file names results.txt in the same directory.

## Views created in the database
One view is created to excute the last query: 
``` sql
CREATE VIEW error_view AS
SELECT DATE(time) AS f_date, SUM(CASE WHEN
    SUBSTRING(status, 0, 4)::INT >= 400
    THEN 1
    ELSE 0
    END)::DECIMAL / (COUNT(log.status))AS f_per
FROM log
GROUP BY DATE(time);
```

## Additional Notes
* You do not need to run the program locally to see the results of the report. The results are placed in the results.txt file in the respository for your viewing convinence. 
