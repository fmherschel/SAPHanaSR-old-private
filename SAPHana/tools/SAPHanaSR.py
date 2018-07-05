# SAPHana.py
#
# Description:	Gets the overall SR status of the local site to
#               a given remote site
#               the script is able to work within muti tenyncy database
#               installations
#
##############################################################################
#
# SAPHana
# Author:       Fabian Herschel, June 2015
# Support:      linux@sap.com
# License:      GNU General Public License (GPL)
# Copyright:    (c) 2015 SUSE Linux GmbH
import sys
import systemReplicationStatus as sr

remSite = sys.argv[1];
noAnswer = 1;
worstStatus=0
rc = 2;

# rc:
# 0 : all SRs for the site are ACTIVE
# 1 : some SRs for the site are not ACTIVE
# 2 : fatal - did not got SRs answer
status2Rc = { "ACTIVE": 0, "SYNCING": 1, "INITIALIZING": 1, "UNKNOWN": 1, "ERROR": 1, "FATAL": 2  }

print "SR for site: " + remSite;

srDict = sr.getLandscapeConfiguration(remSite)[0]
for srEntry in srDict:
     noAnswer = 0
     print srEntry["HOST"] + " / " + str(srEntry["PORT"]) + " / " + srEntry["DATABASE"] + " / " + srEntry["REPLICATION_STATUS"]
     currStatus = status2Rc[srEntry["REPLICATION_STATUS"]];
     print "currStatus " + str(currStatus)
     if ( worstStatus < currStatus ):
         worstStatus = currStatus;

if ( noAnswer == 1 ):
     print "No Answer "
     rc=status2Rc["FATAL"]
else:
     rc=worstStatus

sys.exit(rc)
