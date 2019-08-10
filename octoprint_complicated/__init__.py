# coding=utf-8
from __future__ import absolute_import

import complicated as complicated_lib

import urllib

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class ComplicatedPlugin( octoprint.plugin.ProgressPlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin ):
    config_version_key = '1'

    # #~~ SettingsPlugin mixin

    def get_settings_defaults( self ):
        return dict(
            api_key="Put Your Api Key Here",
            selected_complication="modularLarge",
            value_template="Print {progress}% Completed",
            notfiy_at_50_percent='No',
            notfiy_at_100_percent='No'
        )


    def get_settings_restricted_paths(self):
        return dict(
            admin=[ [ 'api_key' ] ],
            user=[ [ 'selected_complication' ], [ 'value_template' ], [ 'notfiy_at_50_percent' ], [ 'notfiy_at_100_percent' ] ],
            never=[]
        )

    # #~~ 

    def get_template_configs( self ):
		return [
            dict(
                type="settings", 
                name='Complicated Apple Watch', 
                custom_bindings=False
            )
        ]

    def on_print_progress( self, storage, path, progress ):
        if progress < 50:
            self.notified_at_50 = False
            self.notified_at_100 = False

        self._logger.info( 'Updating server with progress {}'.format( progress ) )

        api_key = self._settings.get( [ 'api_key' ] )
        if api_key == "" or api_key == None or len( api_key ) != 8:
            self._logger.info( 'Api Key Not Set, or Invalid' )
            return

        selected_complciation = self._settings.get( [ 'selected_complication' ] )
        if selected_complciation == "" or selected_complciation == None:
            self._logger.info( 'Selected complication not set' )
            return

        value_template = self._settings.get( [ 'value_template' ] )
        if value_template == "" or value_template == None:
            self._logger.info( 'Value template not set' )
            return

        new_value = value_template.replace( "{progress}", str( progress ) )

        self._logger.info( 'settings notify' )
        self._logger.info( self._settings.get( [ 'notfiy_at_50_percent' ] ) )

        alert = None
        if progress >= 50 and not self.notified_at_50 and self._settings.get( [ 'notfiy_at_50_percent' ] ) == 'Yes':
            alert = "Print 50% Complete!"
            self.notified_at_50 = True

        if progress >= 100 and not self.notified_at_100 and self._settings.get( [ 'notfiy_at_100_percent' ] ) == 'Yes':
            alert = "Print 100% Complete!"
            self.notified_at_100 = True

        complicated_lib.changeComplication( api_key, selected_complciation, new_value, alert=alert )

    def get_update_information(self, *args, **kwargs):
        return {
            'octoprint_complicated':{
                'displayName': self._plugin_name,
                'displayVersion': self._plugin_version,
                'type': 'github_release',
                'current': self._plugin_version,
                'user': 'frenchie4111',
                'repo': 'complicated-octoprint',
                'pip': 'https://github.com/frenchie41111/complicated-octoprint/archive/{target}.zip',
            }
        }

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.

__plugin_name__ = 'Complicated Plugin'
__plugin_version__ = '1.1.2'
__plugin_implementation__ = ComplicatedPlugin()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}