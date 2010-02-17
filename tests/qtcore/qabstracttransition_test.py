#!/usr/bin/python
import unittest
from sys import getrefcount
from PySide.QtCore import QObject, SIGNAL, QCoreApplication, QTimer, QVariant
from PySide.QtCore import QState, QFinalState, QStateMachine, QParallelAnimationGroup, QEventTransition

def addStates(transition):
    sx = QState()
    sy = QState()
    transition.setTargetStates([sx, sy])

def addAnimation(transition):
    animation = QParallelAnimationGroup()
    transition.addAnimation(animation)

class QAbstractTransitionTest(unittest.TestCase):

    def testBasic(self):
        app = QCoreApplication([])

        o = QObject()
        o.setProperty("text", QVariant("INdT"))

        machine = QStateMachine()
        s1 = QState()
        s1.assignProperty(o, "text", QVariant("Rocks"))

        s2 = QFinalState()
        t = s1.addTransition(o, SIGNAL("change()"), s2)

        self.assertEqual(t.targetStates(), [s2])

        addStates(t)
        self.assertEqual(len(t.targetStates()), 2)

        animation = QParallelAnimationGroup()
        t.addAnimation(animation)

        self.assertEqual(t.animations(), [animation])

        addAnimation(t)
        self.assertEqual(t.animations()[0].parent(), None)

        machine.addState(s1)
        machine.addState(s2)
        machine.setInitialState(s1)
        machine.start()

        QTimer.singleShot(100, app.quit)
        app.exec_()

    def testRefCountOfTargetState(self):
        transition = QEventTransition()
        state1 = QState()
        refcount1 = getrefcount(state1)
        transition.setTargetState(state1)
        self.assertEqual(transition.targetState(), state1)
        self.assertEqual(getrefcount(transition.targetState()), refcount1 + 1)

        state2 = QState()
        refcount2 = getrefcount(state2)
        transition.setTargetState(state2)
        self.assertEqual(transition.targetState(), state2)
        self.assertEqual(getrefcount(transition.targetState()), refcount2 + 1)
        self.assertEqual(getrefcount(state1), refcount1)

        del transition
        self.assertEqual(getrefcount(state2), refcount2)

if __name__ == '__main__':
    unittest.main()

