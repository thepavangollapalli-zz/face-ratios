import java.awt.Font;
import java.awt.Point;
import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.renderer.category.BoxAndWhiskerRenderer;
import org.jfree.data.statistics.BoxAndWhiskerCategoryDataset;
import org.jfree.data.statistics.DefaultBoxAndWhiskerCategoryDataset;
import org.jfree.ui.ApplicationFrame;

import Luxand.FSDK;
import Luxand.FSDK.FSDK_Features;
import Luxand.FSDK.HImage;

public class FaceRatios {
	private static final String FACE_SDK_LICENSE = "GKoaCTMBfJUe6gxztyVMgZIENNMBox/+p+XGXhNqioF8uzYUu/ksPU548IrFLTbnCny2vAhIxOQhDrSF4qSKFBowDQ62PuRNfygDiZ+tOVQJHdcL+l32KEgHOybMifWNaJb6vy9z1oRKQbk9jm3MzP8zJU0yUL/hZaRde7GlzaY=";
	private static final String FACE_DIRECTORY = "C:\\Users\\susha_000\\workspace2\\FaceDetect\\faces\\";
	private static final String[] propertyNames = new String[] {
		"eyeSize/eyeDistance", "eyeSizeDisparity",
		"eyeDistance/mouthLength", "eyeDistance/noseHeight",
		"eyeSize/mouthLength", "eyeSize/noseHeight",
		"mouthLength/mouthHeight", "chinHeight/noseHeight",
		"chinHeight/chinToBridgeHeight", "noseHeight/chinToBridgeHeight",
		"mouthHeight/chinToBridgeHeight", "faceCountourAngle",
		"bridgeToEyeDisparity"
	};

	@SuppressWarnings("serial")
	public static void main(String[] args) {
		int r = FSDK.ActivateLibrary(FACE_SDK_LICENSE);
		if (r == FSDK.FSDKE_OK) {
			FSDK.Initialize();
			FSDK.SetFaceDetectionParameters(true, true, 384);

			Map<String, Map<String, ArrayList<Double>>> faceProperties = new HashMap<>();

			for (String directory : new File(FACE_DIRECTORY).list()) {
				if (new File(FACE_DIRECTORY + directory).isDirectory()) {
					Map<String, ArrayList<Double>> properties = new HashMap<String, ArrayList<Double>>() {
						{
							for (String property : propertyNames)
								put(property, new ArrayList<Double>());
						}
					};

					File[] files = new File(FACE_DIRECTORY + directory).listFiles();
					System.out.println("Analyzing " + directory + " with " + files.length + " files\n");
					for (File file : files) {
						if (file.isFile()) {
							HImage imageHandle = new HImage();
							FSDK.LoadImageFromFileW(imageHandle, file.getAbsolutePath());

							FSDK.TFacePosition.ByReference facePosition = new FSDK.TFacePosition.ByReference();
							if (FSDK.DetectFace(imageHandle, facePosition) == FSDK.FSDKE_OK) {
								FSDK_Features.ByReference facialFeatures = new FSDK_Features.ByReference();
								FSDK.DetectFacialFeaturesInRegion(imageHandle, (FSDK.TFacePosition) facePosition, facialFeatures);

								Point[] featurePoints = new Point[FSDK.FSDK_FACIAL_FEATURE_COUNT];
								for (int i = 0; i < FSDK.FSDK_FACIAL_FEATURE_COUNT; i++) {
									featurePoints[i] = new Point(0, 0);
									featurePoints[i].x = facialFeatures.features[i].x;
									featurePoints[i].y = facialFeatures.features[i].y;
								}

								double eyeDistance = featureDistance(featurePoints, FeatureID.LEFT_EYE, FeatureID.RIGHT_EYE);
								double rightEyeSize = featureDistance(featurePoints, FeatureID.RIGHT_EYE_INNER_CORNER, FeatureID.RIGHT_EYE_OUTER_CORNER);
								double leftEyeSize = featureDistance(featurePoints, FeatureID.LEFT_EYE_INNER_CORNER, FeatureID.LEFT_EYE_OUTER_CORNER);
								double averageEyeSize = (rightEyeSize + leftEyeSize) / 2;

								double mouthLength = featureDistance(featurePoints, FeatureID.MOUTH_RIGHT_CORNER, FeatureID.MOUTH_LEFT_CORNER);
								double mouthHeight = featureDistance(featurePoints, FeatureID.MOUTH_BOTTOM, FeatureID.MOUTH_TOP);
								double noseHeight = featureDistance(featurePoints, FeatureID.NOSE_BOTTOM, FeatureID.NOSE_BRIDGE);
								double chinHeight = featureDistance(featurePoints, FeatureID.CHIN_BOTTOM, FeatureID.MOUTH_BOTTOM);

								double chinToBridgeHeight = featureDistance(featurePoints, FeatureID.CHIN_BOTTOM, FeatureID.NOSE_BRIDGE);

								double faceContourLeft = (featurePoints[FeatureID.CHIN_BOTTOM.getIndex()].getY() - featurePoints[FeatureID.FACE_CONTOUR2.getIndex()].getY())
									/ (featurePoints[FeatureID.CHIN_BOTTOM.getIndex()].getX() - featurePoints[FeatureID.FACE_CONTOUR2.getIndex()].getX());
								double faceContourRight = (featurePoints[FeatureID.CHIN_BOTTOM.getIndex()].getY() - featurePoints[FeatureID.FACE_CONTOUR12.getIndex()].getY())
									/ (featurePoints[FeatureID.CHIN_BOTTOM.getIndex()].getX() - featurePoints[FeatureID.FACE_CONTOUR12.getIndex()].getX());

								double bridgeLeftEyeDistance = featureDistance(featurePoints, FeatureID.LEFT_EYE_INNER_CORNER, FeatureID.NOSE_BRIDGE);
								double bridgeRightEyeDistance = featureDistance(featurePoints, FeatureID.RIGHT_EYE_INNER_CORNER, FeatureID.NOSE_BRIDGE);

								properties.get("eyeSize/eyeDistance").add(averageEyeSize / eyeDistance);
								properties.get("eyeSizeDisparity").add(Math.abs(leftEyeSize - rightEyeSize) / averageEyeSize);
								properties.get("bridgeToEyeDisparity").add(Math.abs(bridgeLeftEyeDistance - bridgeRightEyeDistance) / ((bridgeLeftEyeDistance + bridgeRightEyeDistance) / 2));
								properties.get("eyeDistance/mouthLength").add(eyeDistance / mouthLength);
								properties.get("eyeDistance/noseHeight").add(eyeDistance / noseHeight);
								properties.get("eyeSize/mouthLength").add(eyeDistance / mouthLength);
								properties.get("eyeSize/noseHeight").add(eyeDistance / noseHeight);
								properties.get("mouthLength/mouthHeight").add(mouthLength / mouthHeight);
								properties.get("chinHeight/noseHeight").add(chinHeight / noseHeight);
								properties.get("chinHeight/chinToBridgeHeight").add(chinHeight / chinToBridgeHeight);
								properties.get("noseHeight/chinToBridgeHeight").add(noseHeight / chinToBridgeHeight);
								properties.get("mouthHeight/chinToBridgeHeight").add(mouthHeight / chinToBridgeHeight);
								properties.get("faceCountourAngle").add(Math.toDegrees(Math.atan((faceContourLeft - faceContourRight) / (1 + faceContourLeft * faceContourRight))));
							}

							FSDK.FreeImage(imageHandle);
						}
					}

					System.out.format("%32s\t%8s\t%8s\t%3s%n", "Property", "μ", "σ", "c");
					System.out.println(new String(new char[76]).replace("\0", "-"));

					ArrayList<Entry<String, ArrayList<Double>>> propertyList = new ArrayList<>(properties.entrySet());
					Collections.sort(propertyList, new Comparator<Entry<String, ArrayList<Double>>>() {
						@Override
						public int compare(Entry<String, ArrayList<Double>> arg0, Entry<String, ArrayList<Double>> arg1) {
							DescriptiveStatistics dStats0 = new DescriptiveStatistics(listToArray(arg0.getValue()));
							DescriptiveStatistics dStats1 = new DescriptiveStatistics(listToArray(arg1.getValue()));
							return new Double(dStats0.getStandardDeviation() / dStats0.getMean()).compareTo(dStats1.getStandardDeviation() / dStats1.getMean());
						}
					});

					for (Entry<String, ArrayList<Double>> property : propertyList) {
						DescriptiveStatistics dStats = new DescriptiveStatistics(listToArray(property.getValue()));
						System.out.format("%32s\t%4f\t%4f\t%3s%n", property.getKey(), dStats.getMean(), dStats.getStandardDeviation(), Math.round(dStats.getStandardDeviation() / dStats.getMean() * 100) + "%");
					}

					System.out.println("\n");
					faceProperties.put(directory, properties);
				}
			}

			for (String propertyName : propertyNames) {
				DefaultBoxAndWhiskerCategoryDataset dataset = new DefaultBoxAndWhiskerCategoryDataset();
				for (Entry<String, Map<String, ArrayList<Double>>> face : faceProperties.entrySet()) {
					dataset.add(face.getValue().get(propertyName), "Default Series", face.getKey());
				}

				PropertyBoxWhisker plot = new PropertyBoxWhisker(propertyName, dataset);
				plot.pack();
				plot.setVisible(true);
			}
		}
	}

	private static double[] listToArray(ArrayList<Double> list) {
		double[] data = new double[list.size()];
		for (int i = 0; i < list.size(); i++)
			data[i] = list.get(i);
		return data;
	}

	private static double featureDistance(Point[] featurePoints, FeatureID f1, FeatureID f2) {
		return distance(featurePoints[f1.getIndex()], featurePoints[f2.getIndex()]);
	}

	private static double distance(Point p1, Point p2) {
		return Math.sqrt(Math.pow(p1.getX() - p2.getX(), 2) + Math.pow(p1.getY() - p2.getY(), 2));
	}
}

@SuppressWarnings("serial")
class PropertyBoxWhisker extends ApplicationFrame {
	public PropertyBoxWhisker(String propertyName, BoxAndWhiskerCategoryDataset dataset) {
		super(propertyName);
		final CategoryAxis xAxis = new CategoryAxis("Face");
		final NumberAxis yAxis = new NumberAxis("Value");
		yAxis.setAutoRangeIncludesZero(false);

		final BoxAndWhiskerRenderer renderer = new BoxAndWhiskerRenderer();
		renderer.setFillBox(false);
		final CategoryPlot plot = new CategoryPlot(dataset, xAxis, yAxis, renderer);
		final JFreeChart chart = new JFreeChart(propertyName, new Font("SansSerif", Font.BOLD, 14), plot, true);
		final ChartPanel chartPanel = new ChartPanel(chart);
		chartPanel.setPreferredSize(new java.awt.Dimension(900, 540));
		setContentPane(chartPanel);
	}
}
