from codecs import latin_1_decode
import libnmea_navsat_driver.parser
from libnmea_navsat_driver.checksum_utils import check_nmea_checksum
import math
import rospy
from sensor_msgs.msg import NavSatFix, NavSatStatus, TimeReference
from geometry_msgs.msg import TwistStamped, QuaternionStamped, Pose
from tf.transformations import quaternion_from_euler
from math import *
import numpy
lonB = 0
latB = 0
latitude = "nan"
longitude = "nan"
i = 0
oldlat = 0
oldlon = 0
class RosNMEADriver(object):
    """ROS driver for NMEA GNSS devices."""

    def __init__(self):
        """Initialize the ROS NMEA driver.

        :ROS Publishers:
            - NavSatFix publisher on the 'fix' channel.
            - TwistStamped publisher on the 'vel' channel.
            - QuaternionStamped publisher on the 'heading' channel.
            - TimeReference publisher on the 'time_reference' channel.

        :ROS Parameters:
            - ~time_ref_source (str)
                The name of the source in published TimeReference messages. (default None)
            - ~useRMC (bool)
                If true, use RMC NMEA messages. If false, use GGA and VTG messages. (default False)
            - ~epe_quality0 (float)
                Value to use for default EPE quality for fix type 0. (default 1000000)
            - ~epe_quality1 (float)
                Value to use for default EPE quality for fix type 1. (default 4.0)
            - ~epe_quality2 (float)
                Value to use for default EPE quality for fix type 2. (default (0.1)
            - ~epe_quality4 (float)
                Value to use for default EPE quality for fix type 4. (default 0.02)
            - ~epe_quality5 (float)
                Value to use for default EPE quality for fix type 5. (default 4.0)
            - ~epe_quality9 (float)
                Value to use for default EPE quality for fix type 9. (default 3.0)
        """
        self.fix_pub = rospy.Publisher('rover/fix', NavSatFix, queue_size=1)
        self.vel_pub = rospy.Publisher('vel', TwistStamped, queue_size=1)
        self.heading_pub = rospy.Publisher(
            'heading', QuaternionStamped, queue_size=1)
        self.use_GNSS_time = rospy.get_param('~use_GNSS_time', False)
        if not self.use_GNSS_time:
            self.time_ref_pub = rospy.Publisher(
                'time_reference', TimeReference, queue_size=1)

        self.time_ref_source = rospy.get_param('~time_ref_source', None)
        self.use_RMC = rospy.get_param('~useRMC', False)
        self.valid_fix = False

        # epe = estimated position error
        self.default_epe_quality0 = rospy.get_param('~epe_quality0', 1000000)
        self.default_epe_quality1 = rospy.get_param('~epe_quality1', 4.0)
        self.default_epe_quality2 = rospy.get_param('~epe_quality2', 0.1)
        self.default_epe_quality4 = rospy.get_param('~epe_quality4', 0.02)
        self.default_epe_quality5 = rospy.get_param('~epe_quality5', 4.0)
        self.default_epe_quality9 = rospy.get_param('~epe_quality9', 3.0)
        self.using_receiver_epe = False

        self.lon_std_dev = float("nan")
        self.lat_std_dev = float("nan")
        self.alt_std_dev = float("nan")

        """Format for this dictionary is the fix type from a GGA message as the key, with
        each entry containing a tuple consisting of a default estimated
        position error, a NavSatStatus value, and a NavSatFix covariance value."""
        self.gps_qualities = {
            # Unknown
            -1: [
                self.default_epe_quality0,
                NavSatStatus.STATUS_NO_FIX,
                NavSatFix.COVARIANCE_TYPE_UNKNOWN
            ],
            # Invalid
            0: [
                self.default_epe_quality0,
                NavSatStatus.STATUS_NO_FIX,
                NavSatFix.COVARIANCE_TYPE_UNKNOWN
            ],
            # SPS
            1: [
                self.default_epe_quality1,
                NavSatStatus.STATUS_FIX,
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            ],
            # DGPS
            2: [
                self.default_epe_quality2,
                NavSatStatus.STATUS_SBAS_FIX,
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            ],
            # RTK Fix
            4: [
                self.default_epe_quality4,
                NavSatStatus.STATUS_GBAS_FIX,
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            ],
            # RTK Float
            5: [
                self.default_epe_quality5,
                NavSatStatus.STATUS_GBAS_FIX,
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            ],
            # WAAS
            9: [
                self.default_epe_quality9,
                NavSatStatus.STATUS_GBAS_FIX,
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED
            ]
        }

    def add_sentence(self, nmea_string, frame_id, timestamp=None):
        """Public method to provide a new NMEA sentence to the driver.

        Args:
            nmea_string (str): NMEA sentence in string form.
            frame_id (str): TF frame ID of the GPS receiver.
            timestamp(rospy.Time, optional): Time the sentence was received.
                If timestamp is not specified, the current time is used.

        Returns:
            bool: True if the NMEA string is successfully processed, False if there is an error.
        """
        if not check_nmea_checksum(nmea_string):
            rospy.logwarn("Received a sentence with an invalid checksum. " +
                          "Sentence was: %s" % repr(nmea_string))
            return False

        parsed_sentence = libnmea_navsat_driver.parser.parse_nmea_sentence(
            nmea_string)
        if not parsed_sentence:
            rospy.logdebug(
                "Failed to parse NMEA sentence. Sentence was: %s" %
                nmea_string)
            return False

        if timestamp:
            current_time = timestamp
        else:
            current_time = rospy.get_rostime()
        current_fix = NavSatFix()
        current_fix.header.stamp = current_time
        current_fix.header.frame_id = frame_id
        if not self.use_GNSS_time:
            current_time_ref = TimeReference()
            current_time_ref.header.stamp = current_time
            current_time_ref.header.frame_id = frame_id
            if self.time_ref_source:
                current_time_ref.source = self.time_ref_source
            else:
                current_time_ref.source = frame_id

        if not self.use_RMC and 'GGA' in parsed_sentence:
            current_fix.position_covariance_type = \
                NavSatFix.COVARIANCE_TYPE_APPROXIMATED

            data = parsed_sentence['GGA']

            if self.use_GNSS_time:
                if math.isnan(data['utc_time'][0]):
                    rospy.logwarn("Time in the NMEA sentence is NOT valid")
                    return False
                current_fix.header.stamp = rospy.Time(
                    data['utc_time'][0], data['utc_time'][1])

            fix_type = data['fix_type']
            if not (fix_type in self.gps_qualities):
                fix_type = -1
            gps_qual = self.gps_qualities[fix_type]
            default_epe = gps_qual[0]
            current_fix.status.status = gps_qual[1]
            current_fix.position_covariance_type = gps_qual[2]

            self.valid_fix = (fix_type > 0)

            current_fix.status.service = NavSatStatus.SERVICE_GPS

            latitude = data['latitude']
            if data['latitude_direction'] == 'S':
                latitude = -latitude
            current_fix.latitude = latitude

            longitude = data['longitude']
            if data['longitude_direction'] == 'W':
                longitude = -longitude
            current_fix.longitude = longitude

            # Altitude is above ellipsoid, so adjust for mean-sea-level
            altitude = data['altitude'] + data['mean_sea_level']
            current_fix.altitude = altitude

            # use default epe std_dev unless we've received a GST sentence with
            # epes
            if not self.using_receiver_epe or math.isnan(self.lon_std_dev):
                self.lon_std_dev = default_epe
            if not self.using_receiver_epe or math.isnan(self.lat_std_dev):
                self.lat_std_dev = default_epe
            if not self.using_receiver_epe or math.isnan(self.alt_std_dev):
                self.alt_std_dev = default_epe * 2

            hdop = data['hdop']
            current_fix.position_covariance[0] = (hdop * self.lon_std_dev) ** 2
            current_fix.position_covariance[4] = (hdop * self.lat_std_dev) ** 2
            current_fix.position_covariance[8] = (
                2 * hdop * self.alt_std_dev) ** 2  # FIXME

            self.fix_pub.publish(current_fix)

            if not (math.isnan(data['utc_time'][0]) or self.use_GNSS_time):
                current_time_ref.time_ref = rospy.Time(
                    data['utc_time'][0], data['utc_time'][1])
                self.last_valid_fix_time = current_time_ref
                self.time_ref_pub.publish(current_time_ref)

        elif not self.use_RMC and 'VTG' in parsed_sentence:
            data = parsed_sentence['VTG']

            # Only report VTG data when you've received a valid GGA fix as
            # well.
            if self.valid_fix:
                current_vel = TwistStamped()
                current_vel.header.stamp = current_time
                current_vel.header.frame_id = frame_id
                current_vel.twist.linear.x = data['speed'] * \
                    math.sin(data['true_course'])
                current_vel.twist.linear.y = data['speed'] * \
                    math.cos(data['true_course'])
                self.vel_pub.publish(current_vel)

        elif 'RMC' in parsed_sentence:
            data = parsed_sentence['RMC']

            if self.use_GNSS_time:
                if math.isnan(data['utc_time'][0]):
                    rospy.logwarn("Time in the NMEA sentence is NOT valid")
                    return False
                current_fix.header.stamp = rospy.Time(
                    data['utc_time'][0], data['utc_time'][1])

            # Only publish a fix from RMC if the use_RMC flag is set.
            if self.use_RMC:
                if data['fix_valid']:
                    current_fix.status.status = NavSatStatus.STATUS_FIX
                else:
                    current_fix.status.status = NavSatStatus.STATUS_NO_FIX

                current_fix.status.service = NavSatStatus.SERVICE_GPS

                latitude = data['latitude']
                if data['latitude_direction'] == 'S':
                    latitude = -latitude
                current_fix.latitude = latitude

                longitude = data['longitude']
                if data['longitude_direction'] == 'W':
                    longitude = -longitude
                current_fix.longitude = longitude

                current_fix.altitude = float('NaN')
                current_fix.position_covariance_type = \
                    NavSatFix.COVARIANCE_TYPE_UNKNOWN

                self.fix_pub.publish(current_fix)

                if not (math.isnan(data['utc_time'][0]) or self.use_GNSS_time):
                    current_time_ref.time_ref = rospy.Time(
                        data['utc_time'][0], data['utc_time'][1])
                    self.time_ref_pub.publish(current_time_ref)

            # Publish velocity from RMC regardless, since GGA doesn't provide
            # it.
            if data['fix_valid']:
                current_vel = TwistStamped()
                current_vel.header.stamp = current_time
                current_vel.header.frame_id = frame_id
                current_vel.twist.linear.x = data['speed'] * \
                    math.sin(data['true_course'])
                current_vel.twist.linear.y = data['speed'] * \
                    math.cos(data['true_course'])
                self.vel_pub.publish(current_vel)
        elif 'GST' in parsed_sentence:
            data = parsed_sentence['GST']

            # Use receiver-provided error estimate if available
            self.using_receiver_epe = True
            self.lon_std_dev = data['lon_std_dev']
            self.lat_std_dev = data['lat_std_dev']
            self.alt_std_dev = data['alt_std_dev']
        elif 'HDT' in parsed_sentence:
            data = parsed_sentence['HDT']
            if data['heading']:
                current_heading = QuaternionStamped()
                current_heading.header.stamp = current_time
                current_heading.header.frame_id = frame_id
                q = quaternion_from_euler(0, 0, math.radians(data['heading']))
                current_heading.quaternion.x = q[0]
                current_heading.quaternion.y = q[1]
                current_heading.quaternion.z = q[2]
                current_heading.quaternion.w = q[3]
                self.heading_pub.publish(current_heading)
        else:
            return False
        global i
        global lonB
        global latB
        global oldlat
        global oldlon
# my code is here
        if current_fix.latitude == 0:
            print("GPS not connected with satellite")
            lat1 = oldlat
            lon1 = oldlon
        else:
            lat1 = current_fix.latitude
            lon1 = current_fix.longitude
            if i<1:
                print("Enter the Goal Location GPS coordinates")
                latB = float(input("Enter Latitude:"))
                lonB = float(input("Enter Longitude:"))
                i = i+ 1
            distance_pub = rospy.Publisher('/distance', Pose, queue_size=50)

            # rospy.Subscriber('/fix', NavSatFix, get_xy_based_on_lat_long, distance_pub)
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lonB, latB])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            x = cos(lat2) * sin(dlon)
            y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            brng = numpy.arctan2(x, y)
            brng = numpy.degrees(brng)
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            Base = 6371 * c
            pose = Pose()
            pose.position.x = Base*1000
            pose.position.y = current_fix.latitude
            pose.position.z = current_fix.longitude
            pose.orientation.x = 0
            pose.orientation.y = brng
            distance_pub.publish(pose)
            rospy.loginfo(pose)
            print("\n")
            oldlon = current_fix.longitude
            oldlat = current_fix.latitude

    @staticmethod
    def get_frame_id():
        """Get the TF frame_id.

        Queries rosparam for the ~frame_id param. If a tf_prefix param is set,
        the frame_id is prefixed with the prefix.

        Returns:
            str: The fully-qualified TF frame ID.
        """
        frame_id = rospy.get_param('~frame_id', 'gps')
        # Add the TF prefix
        prefix = ""
        prefix_param = rospy.search_param('tf_prefix')
        if prefix_param:
            prefix = rospy.get_param(prefix_param)
            return "%s/%s" % (prefix, frame_id)
        else:
            return frame_id
