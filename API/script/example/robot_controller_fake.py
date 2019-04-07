class RobotController():
    def __init__(self, address, machineType):
        pass

    def goPos(self, pos, error=None, type="go", timeout=30, handModeFlag=None):
        print("goPos func", pos, error, type, timeout)

    def goDeltaPos(self, deltaPos, error=None, type="go", timeout=30):
        print("goDeltaPos func", deltaPos)

    def getCurJointAngle(self):
        print("getCurJointAngle func")