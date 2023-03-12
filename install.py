import launch

if not launch.is_installed("pilgram"):
	launch.run_pip("install pilgram", "pilgram")