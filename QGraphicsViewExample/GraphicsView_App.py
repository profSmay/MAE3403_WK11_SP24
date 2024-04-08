#region imports
from GraphicsView_GUI import Ui_Form
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import math
import sys
#endregion

#region class definitions
class MainWindow(Ui_Form, qtw.QWidget):
    def __init__(self):
        """
        This program illustrates the use of the graphics view framework.  The QGraphicsView widget is created in
        designer.  The QGraphicsView displays a QGraphicsScene.  A QGraphicsScene contains QGraphicsItem objects.
        """
        super().__init__()
        self.setupUi(self)
        #region UserInterface stuff here

        #set up graphics view, add a scene and build pens and brushes
        self.setupGraphics()

        #turning on mouse tracking
        self.gv_Main.setMouseTracking(True)
        self.pushButton.setMouseTracking(True)
        self.setMouseTracking(True)

        #draws a scene
        self.buildScene()

        #signals/slots
        self.spnd_Zoom.valueChanged.connect(self.setZoom)
        self.pushButton.clicked.connect(self.pickAColor)
        self.scene.installEventFilter(self)
        self.mouseDown = False
        self.show()

    def setupGraphics(self):
        #create a scene object
        self.scene = qtw.QGraphicsScene()
        self.scene.setObjectName("MyScene")
        self.scene.setSceneRect(-200, -200, 400, 400)  # xLeft, yTop, Width, Height

        #set the scene for the graphics view object
        self.gv_Main.setScene(self.scene)
        #make some pens and brushes for my drawing
        self.setupPensAndBrushes()

    def setupPensAndBrushes(self):
        #make the pens first
        #a thick green pen
        self.penThick = qtg.QPen(qtc.Qt.darkGreen)
        self.penThick.setWidth(5)
        #a medium blue pen
        self.penMed = qtg.QPen(qtc.Qt.darkBlue)
        self.penMed.setStyle(qtc.Qt.SolidLine)
        self.penMed.setWidth(2)
        #a pen for the grid lines
        self.penGridLines = qtg.QPen()
        self.penGridLines.setWidth(1)
        self.penGridLines.setColor(qtg.QColor.fromHsv(197, 144, 228, 255))

        #now make some brushes
        #build a brush for filling with solid red
        self.brushFill = qtg.QBrush(qtc.Qt.darkRed)
        #a brush that makes a hatch pattern
        self.brushHatch = qtg.QBrush()
        self.brushHatch.setStyle(qtc.Qt.DiagCrossPattern)
        #a brush for the background of my grid
        self.brushGrid = qtg.QBrush(qtg.QColor.fromHsv(87, 98, 245, 255))

    def mouseMoveEvent(self, a0: qtg.QMouseEvent):
        w=app.widgetAt(a0.globalPos())
        if w is None:
            name='none'
        else:
            name=w.objectName()
        self.setWindowTitle(str(a0.x())+','+ str(a0.y())+name)

    def eventFilter(self, obj, event):
        # I set up an event filter to track mouse position and illustrate difference between scene and screen coords.
        if obj == self.scene:
            et=event.type()
            if event.type() == qtc.QEvent.GraphicsSceneMouseMove:
                w=app.topLevelAt(event.screenPos())
                screenPos=event.screenPos()
                scenePos=event.scenePos()
                strScreen="screen x = {}, screen y = {}".format(screenPos.x(), screenPos.y())
                strScene=":  scene x = {}, scene y = {}".format(scenePos.x(), scenePos.y())
                self.setWindowTitle(strScreen+strScene)
                if self.mouseDown:
                    scenePos = event.scenePos()
                    centerX = self.tmpCircle.rect().center().x()
                    centerY = self.tmpCircle.rect().center().y()
                    radius = math.pow(centerX-scenePos.x(),2)+math.pow(centerY-scenePos.y(),2)
                    radius = math.sqrt(radius)
                    self.tmpCircle.setRect(centerX-radius, centerY-radius, 2*radius, 2*radius)
                    self.tmpLn.setLine(centerX, centerY, scenePos.x(),scenePos.y())

            if event.type() == qtc.QEvent.GraphicsSceneWheel:
                if event.delta()>0:
                    self.spnd_Zoom.stepUp()
                else:
                    self.spnd_Zoom.stepDown()
            if event.type() ==qtc.QEvent.GraphicsSceneMousePress:
                if event.button() ==qtc.Qt.LeftButton:
                    pos = event.screenPos()
                    scenePos = event.scenePos()
                    self.tmpCircle = self.drawACircle(scenePos.x(),scenePos.y(),1)
                    self.tmpLn = self.drawALine(scenePos.x(), scenePos.y(), scenePos.x()+1, scenePos.y()+1)
                    self.tmpCircle.setPen(self.penMed)
                    self.tmpCircle.setBrush(self.brushGrid)
                    self.tmpLn.setPen(self.penGridLines)
                    self.mouseDown = True
            if event.type() == qtc.QEvent.GraphicsSceneMouseRelease:
                self.mouseDown = False
        # pass the event along to the parent widget if there is one.
        return super(MainWindow, self).eventFilter(obj, event)

    def buildScene(self):
        #clear out the old scene first
        self.scene.clear()

        #draw a grid
        self.drawAGrid(DeltaX=10, DeltaY=10, Height=200, Width=200, Pen=self.penGridLines, Brush=self.brushGrid)

        #draw some lines
        self.line1 = self.drawALine(-50, -50, -50, 50)
        self.line1.setPen(self.penThick)
        self.line2 = self.drawALine(-50, -50, 50, -50)
        self.line2.setPen(self.penThick)

        self.drawACircle(-50,-50,5, pen=self.penMed, brush=self.brushFill)
        self.drawASquare(-50,50,10, pen=self.penMed, brush=self.brushFill)
        self.drawATriangle(50,-50,10, pen=self.penMed, brush=self.brushHatch)
        self.drawAnArrow(0,0,10,-20,pen=self.penMed, brush=self.brushFill)

    def drawAGrid(self, DeltaX=10, DeltaY=10, Height=200, Width=200, CenterX=0, CenterY=0, Pen=None, Brush=None, SubGrid=None):
        """
        This makes a grid for reference.  No snapping to grid enabled.
        :param DeltaX: grid spacing in x direction
        :param DeltaY: grid spacing in y direction
        :param Height: height of grid (y)
        :param Width: width of grid (x)
        :param CenterX: center of grid (x, in scene coords)
        :param CenterY: center of grid (y, in scene coords)
        :param Pen: pen for grid lines
        :param Brush: brush for background
        :param SubGrid: subdivide the grid (not currently working)
        :return: nothing
        """
        height = self.scene.sceneRect().height() if Height is None else Height
        width = self.scene.sceneRect().width() if Width is None else Width
        left = self.scene.sceneRect().left() if CenterX is None else (CenterX - width / 2.0)
        right = self.scene.sceneRect().right() if CenterX is None else (CenterX + width / 2.0)
        top = self.scene.sceneRect().top() if CenterY is None else (CenterY - height / 2.0)
        bottom = self.scene.sceneRect().bottom() if CenterY is None else (CenterY + height / 2.0)
        Dx = DeltaX
        Dy = DeltaY
        pen = qtg.QPen() if Pen is None else Pen

        # make the background rectangle first
        if Brush is not None:
            rect = self.drawARectangle(left, top, width, height)
            rect.setBrush(Brush)
            rect.setPen(pen)
        # draw the vertical grid lines
        x = left
        while x <= right:
            lVert = self.drawALine(x, top, x, bottom)
            lVert.setPen(pen)
            x += Dx
        # draw the horizontal grid lines
        y = top
        while y <= bottom:
            lHor = self.drawALine(left, y, right, y)
            lHor.setPen(pen)
            y += Dy

    def drawARectangle(self, leftX, topY, widthX, heightY):
        rect = qtw.QGraphicsRectItem(leftX,topY,widthX,heightY)
        self.scene.addItem(rect)
        return rect
    def drawALine(self, stX, stY, enX, enY):
        line = qtw.QGraphicsLineItem(stX, stY, enX, enY)
        self.scene.addItem(line)
        return line

    def polarToRect(self, centerX, centerY, radius, angleDeg=0):
        angleRad=angleDeg*2.0*math.pi/360.0
        return centerX+radius*math.cos(angleRad), centerY+radius*math.sin(angleRad)

    def drawACircle(self, centerX, centerY, Radius, angle=0, brush=None, pen=None):
        ellipse=qtw.QGraphicsEllipseItem(centerX-Radius, centerY-Radius,2*Radius, 2*Radius)
        if pen is not None:
            ellipse.setPen(pen)
        if brush is not None:
            ellipse.setBrush(brush)
        self.scene.addItem(ellipse)
        return ellipse

    def drawASquare(self, centerX, centerY, Size, brush=None, pen=None):
        sqr=qtw.QGraphicsRectItem(centerX-Size/2.0, centerY-Size/2.0, Size, Size)
        if pen is not None:
            sqr.setPen(pen)
        if brush is not None:
            sqr.setBrush(brush)
        self.scene.addItem(sqr)
        return sqr

    def drawATriangle(self, centerX, centerY, Radius, angleDeg=0,brush=None, pen=None):
        pts=[]

        x,y=self.polarToRect(centerX,centerY,Radius, 0+angleDeg)
        pts.append(qtc.QPointF(x,y))
        x,y=self.polarToRect(centerX,centerY,Radius,120+angleDeg)
        pts.append(qtc.QPointF(x,y))
        x,y=self.polarToRect(centerX, centerY,Radius,240+angleDeg)
        pts.append(qtc.QPointF(x,y))
        x,y=self.polarToRect(centerX,centerY,Radius,0+angleDeg)
        pts.append(qtc.QPointF(x,y))

        pg=qtg.QPolygonF(pts)
        PG=qtw.QGraphicsPolygonItem(pg)
        if pen is not None:
            PG.setPen(pen)
        if brush is not None:
            PG.setBrush(brush)
        self.scene.addItem(PG)
        return PG

    def drawAnArrow(self, startX, startY, endX, endY, pen=None, brush=None):
        line=qtw.QGraphicsLineItem(startX, startY, endX, endY)
        p=qtg.QPen() if pen is None else pen
        line.setPen(pen)
        angleDeg=180.0/math.pi*math.atan((endY-startY)/(endX-startX))
        self.scene.addItem(line)
        self.drawATriangle(endX, endY, 5, angleDeg=angleDeg,pen=pen, brush=brush)

    def pickAColor(self):
        cdb=qtw.QColorDialog(self)
        c=cdb.getColor()
        hsv=c.getHsv()
        self.pushButton.setText(str(hsv))
        self.penGridLines.setColor(qtg.QColor.fromHsv(hsv[0],hsv[1],hsv[2],hsv[3]))
        self.buildScene()
        pass

    def setZoom(self):
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())
#endregion

#region function calls
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('GraphicsView')
    sys.exit(app.exec())
#endregion