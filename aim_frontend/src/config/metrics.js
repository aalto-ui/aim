export default {
  categories: [
    {
      name: 'Colour Perception',
      id: 'cp',
      color: 'cat-one',
      metrics: [
        'cp1',
        'cp2',
        'cp3',
        'cp4',
        'cp5',
        'cp6',
        'cp7',
        'cp8',
        'cp9',
        'cp10'
      ]
    },
    {
      name: 'Perceptual Fluency',
      id: 'pf',
      color: 'cat-two',
      metrics: [
        'pf1',
        'pf2',
        'pf3',
        'pf4',
        'pf5',
        'pf6',
        'pf7',
        'pf8'
      ]
    },
    {
      name: 'Visual Guidance',
      id: 'vg',
      color: 'cat-three',
      metrics: [
        'vg1',
        'vg2'
      ]
    },
    {
      name: 'Accessibility',
      id: 'ac',
      color: 'cat-four',
      metrics: [
        'ac1'
      ]
    }
  ],
  metrics: {
    cp1: {
      id: 'cp1',
      name: 'PNG File Size',
      category: 'cp',
      description: 'File size in PNG indicates the number of effectively used colors. The higher the size, the more colourful the image is likely to be. Note that this is confounded by other factors, such as image complexity.',
      evidence: 1,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'cp1_0',
          index: 0,
          type: 'int',
          name: 'PNG File Size (in bytes)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 500000],
              description: 'Suitable'
            },
            {
              id: 'r2',
              range: [500001, 1200000],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [1200001, null],
              description: 'Huge'
            }
          ]
        }
      ]
    },
    cp2: {
      id: 'cp2',
      name: 'Unique RGB colours',
      category: 'cp',
      description: 'The number of unique colours in RGB spectrum is an indication of colour variance. Colours that occur more than a threshold value are counted. Note that this is confounded by image size',
      evidence: 2,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        },
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        }
      ],
      results: [
        {
          id: 'cp2_0',
          index: 0,
          type: 'int',
          name: 'Number of Colours',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 5000],
              description: 'Less colorful'
            },
            {
              id: 'r2',
              range: [5001, 15000],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [15001, null],
              description: 'Colourful'
            }
          ]
        }
      ]
    },
    cp3: {
      id: 'cp3',
      name: 'HSV colours: Average and std',
      category: 'cp',
      description: 'The HSV (Hue, Saturation, Value) colour space aligns more closely with the human visual system. These metrics report average and standard deviation for each channel in HSV. Empirical research has shown hue and saturation channels to correlated with aesthetic impression.',
      evidence: 3,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Hasler, D. and Süsstrunk, S. Measuring Colourfuness in Natural Images.',
          fileName: 'hasler_and_susstrunk_2003.pdf'
        }
      ],
      results: [
        {
          id: 'cp3_0',
          index: 0,
          type: 'float',
          name: 'Average Hue',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp3_1',
          index: 1,
          type: 'float',
          name: 'Average Saturation',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.10],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [0.11, 0.60],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [0.61, null],
              description: 'High'
            }
          ]
        },
        {
          id: 'cp3_2',
          index: 2,
          type: 'float',
          name: 'Standard Deviation of Saturation',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.20],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [0.21, 0.40],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [0.41, null],
              description: 'High'
            }
          ]
        },
        {
          id: 'cp3_3',
          index: 3,
          type: 'float',
          name: 'Average Value',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.40],
              description: 'Dark'
            },
            {
              id: 'r2',
              range: [0.41, 0.80],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [0.81, 1.00],
              description: 'Light'
            }
          ]
        },
        {
          id: 'cp3_4',
          index: 4,
          type: 'float',
          name: 'Standard Deviation of Value',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.15],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [0.16, 0.35],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [0.36, null],
              description: 'High'
            }
          ]
        }
      ]
    },
    cp4: {
      id: 'cp4',
      name: 'Number of unique colours in the HSV spectrum',
      category: 'cp',
      description: 'The HSV (Hue, Saturation, Value) colour space aligns more closely with the human visual system.  This metric reports the number of unique colours per channel in HSV. Unlike the other HSV metric, no direct empirical evidence exists for this metric. Note that the metric correlates highly with the number of colours in the RGB space.',
      evidence: 2,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Hasler, D. and Süsstrunk, S. Measuring Colourfuness in Natural Images.',
          fileName: 'hasler_and_susstrunk_2003.pdf'
        }
      ],
      results: [
        {
          id: 'cp4_0',
          index: 0,
          type: 'int',
          name: 'Number of Unique HSV',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 20000],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [20001, null],
              description: 'Potential varied'
            }
          ]
        },
        {
          id: 'cp4_1',
          index: 1,
          type: 'int',
          name: 'Number of Unique Hue',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp4_2',
          index: 2,
          type: 'int',
          name: 'Number of Unique Saturation',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp4_3',
          index: 3,
          type: 'int',
          name: 'Number of Unique Value',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        }
      ]
    },
    cp5: {
      id: 'cp5',
      name: 'LAB colours',
      category: 'cp',
      description: 'The LAB colour space approximates human vision for uniformity of colour perception. Results sre similar to the HSV metric. Empirical work has provided support for correlation between SD in luminance and aesthetic impression.',
      evidence: 3,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Hasler, D. and Süsstrunk, S. Measuring Colourfuness in Natural Images.',
          fileName: 'hasler_and_susstrunk_2003.pdf'
        }
      ],
      results: [
        {
          id: 'cp5_0',
          index: 0,
          type: 'float',
          name: 'Mean Lightness',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 40.00],
              description: 'Dark'
            },
            {
              id: 'r2',
              range: [40.01, 75.00],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [75.01, 100.00],
              description: 'Light'
            }
          ]
        },
        {
          id: 'cp5_1',
          index: 1,
          type: 'float',
          name: 'Standard Deviation Lightness',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 15.00],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [15.01, 35.00],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [35.01, null],
              description: 'High'
            }
          ]
        },
        {
          id: 'cp5_2',
          index: 2,
          type: 'float',
          name: 'Mean A (Green-Red Space)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp5_3',
          index: 3,
          type: 'float',
          name: 'Standard Deviation A',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp5_4',
          index: 4,
          type: 'float',
          name: 'Mean B (Yellow-Blue Space)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp5_5',
          index: 5,
          type: 'float',
          name: 'Standard Deviation B',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        }
      ]
    },
    cp6: {
      id: 'cp6',
      name: 'Hassler-Susstrunk colourfulness',
      category: 'cp',
      description: 'The Hassler-Susstrunk metric is computed based on the RGYB colour spectrum and mainly comprises standard deviations. The higher the deviation, the more colourful the image is perceived. This has a high correlation with aesthetic impression, but has been mainly tested with photography not user interfaces. The metric is, however, computationally expensive. Note that this metric does not take hue into account.',
      evidence: 4,
      relevance: 3,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Hasler, D. and Süsstrunk, S. Measuring Colourfuness in Natural Images.',
          fileName: 'hasler_and_susstrunk_2003.pdf'
        }
      ],
      results: [
        {
          id: 'cp6_0',
          index: 0,
          type: 'float',
          name: 'Mean Distribution (Red-Green)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_1',
          index: 1,
          type: 'float',
          name: 'Standard Deviation Distribution (Red-Green)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_2',
          index: 2,
          type: 'float',
          name: 'Mean Distribution (Yellow-Blue)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_3',
          index: 3,
          type: 'float',
          name: 'Standard Deviation Distribution (Yellow-Blue)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_4',
          index: 4,
          type: 'float',
          name: 'Mean Distribution (RGYB)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_5',
          index: 5,
          type: 'float',
          name: 'Standard Deviation Distribution (RGYB)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        },
        {
          id: 'cp6_6',
          index: 6,
          type: 'float',
          name: 'Colorfulness',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 50.00],
              description: 'Less colorful'
            },
            {
              id: 'r2',
              range: [50.01, 100.00],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [100.01, null],
              description: 'Colorful'
            }
          ]
        }
      ]
    },
    cp7: {
      id: 'cp7',
      name: 'Static colour clustering',
      category: 'cp',
      description: 'Static colour clusters refers to the number of pre-determined colour clusters in the image. Clustering is based on slicing of RGB channels. It indicates the number of dominant colours but is confounded by colour variance.  Dynamic colour clusters has higher correlation with aesthetic impression, but it is also more complex to compute.',
      evidence: 2,
      relevance: 3,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        },
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        }
      ],
      results: [
        {
          id: 'cp7_0',
          index: 0,
          type: 'int',
          name: 'Number of Clusters',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 4000],
              description: 'Less colorful'
            },
            {
              id: 'r2',
              range: [4001, 8000],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [8001, null],
              description: 'Colorful'
            }
          ]
        }
      ]
    },
    cp8: {
      id: 'cp8',
      name: 'Dynamic colour clusters',
      category: 'cp',
      description: 'Indicates the number of color clusters in an image and the average number of colours within each cluster. Colours are clustered recursively, using as criteria their distance in a colour cube. Only clusters with more than 5 values are included in the final count. The number of colours per cluster is shown to correlate with aesthetic perception. Indicates the number of color clusters in an image and the average number of colours within each cluster. Colours are clustered recursively, using as criteria their distance in a colour cube. Only clusters with more than 5 values are included in the final count. The number of colours per cluster is shown to correlate with aesthetic perception.',
      evidence: 3,
      relevance: 3,
      speed: 0,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        },
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        }
      ],
      results: [
        {
          id: 'cp8_0',
          index: 0,
          type: 'int',
          name: 'Number of Clusters',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 500],
              description: 'Less colorful'
            },
            {
              id: 'r2',
              range: [501, 1000],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [1001, null],
              description: 'Colorful'
            }
          ]
        },
        {
          id: 'cp8_1',
          index: 1,
          type: 'int',
          name: 'Average Number of Colours per Cluster',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'Meaningless'
            }
          ]
        }
      ]
    },
    cp9: {
      id: 'cp9',
      name: 'Luminance: Standard deviation',
      category: 'cp',
      description: 'Standard deviation of luminance indicates how much luminance varies across the image. It has no or low correlation with perceived colour variability, but some correlation with aesthetic impression. Note that this implementation does not account for display-dependent gamma corrections (rec. 709 standard).',
      evidence: 3,
      relevance: 3,
      speed: 1,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        }
      ],
      results: [
        {
          id: 'cp9_0',
          index: 0,
          type: 'float',
          name: 'Standard Deviation in Luminance',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 60.00],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [60.01, 90.00],
              description: 'Acceptable'
            },
            {
              id: 'r3',
              range: [90.01, null],
              description: 'Potential varied'
            }
          ]
        }
      ]
    },
    cp10: {
      id: 'cp10',
      name: 'WAVE (Weighted Affective Valence Estimates)',
      category: 'cp',
      description: 'This takes the mean color preference score of each pixel, based on empirically-obtained color preference scores. These color preference scores were retrieved by asking participants to rate their preferences for objects of these colors, with the theory that the preferences for these objects translate directly to preferences for the colors of these objects.',
      evidence: 3,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Palmer, S.E. and Schloss, K.B. An Ecological Valence Theory of Human Color Preference.',
          fileName: 'palmer_and_schloss_2010.pdf'
        }
      ],
      results: [
        {
          id: 'cp10_0',
          index: 0,
          type: 'float',
          name: 'Average WAVE Score Across Pixels',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.54],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [0.55, 1.00],
              description: 'Good'
            }
          ]
        }
      ]
    },
    pf1: {
      id: 'pf1',
      name: 'Edge Density',
      category: 'pf',
      description: 'Edge density correlates with perception of clutter. It is computed as the ratio of pixels that align with an edge as compared to the total number of pixels in the image. Note that this metric does not take colour variance into account, unlike e.g. the feature congestion metric.',
      evidence: 4,
      relevance: 3,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        },
        {
          title: 'Rosenholtz, R., Li, Y., and Nakano, L. Measuring Visual Clutter.',
          fileName: 'rosenholtz_et_al_2007.pdf'
        }
      ],
      results: [
        {
          id: 'pf1_0',
          index: 0,
          type: 'float',
          name: 'Edge Density',
          description: 'Ratio between number of edge pixels and total number of pixels.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.12],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [0.13, 0.22],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [0.23, null],
              description: 'Poor'
            }
          ]
        }
      ]
    },
    pf2: {
      id: 'pf2',
      name: 'Edge Congestion',
      category: 'pf',
      description: 'Edge congestion indicates the ease with which main edges can he perceived. A crowded image is hard to follow. The edge congestion indicator is important for complex interfaces and graph visualizations.',
      evidence: 3,
      relevance: 3,
      speed: 1,
      visualizationType: 'table',
      references: [
        {
          title: 'Levi, D.M. Crowding--An Essential Bottleneck for Object Recognition: A Mini-Review.',
          fileName: 'levi_2008.pdf'
        },
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        },
        {
          title: 'van den Berg, R., Cornelissen, F.W., and Roerdink, J.B.T.M. A Crowding Model of Visual Clutter.',
          fileName: 'van_den_berg_et_al_2009.pdf'
        },
        {
          title: 'Wong, N., Carpendale, S., and Greenberg, S. Edgelens: An Interactive Method for Managing Edge Congestion in Graphs.',
          fileName: 'wong_et_al_2003.pdf'
        }
      ],
      results: [
        {
          id: 'pf2_0',
          index: 0,
          type: 'float',
          name: 'Edge Congestion',
          description: 'Number of congested pixels divided by number of edge pixels.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.25],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [0.26, 0.50],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [0.51, null],
              description: 'Poor'
            }
          ]
        }
      ]
    },
    pf3: {
      id: 'pf3',
      name: 'JPG File Size',
      category: 'pf',
      description: 'JPG file size has some association with clutter perception. However, little evidence exists, and the metric is confounded by other factors.',
      evidence: 2,
      relevance: 3,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'pf3_0',
          index: 0,
          type: 'int',
          name: 'JPEG File Size (in bytes)',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0, 100000],
              description: 'Suitable'
            },
            {
              id: 'r2',
              range: [100001, 200000],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [200001, null],
              description: 'Huge'
            }
          ]
        }
      ]
    },
    pf4: {
      id: 'pf4',
      name: 'Figure-Ground Contrast',
      category: 'pf',
      description: 'Luminance and colour contrast correlates with perceptual fluency. Words and objects with high contrast are easier to read and detect. ',
      evidence: 3,
      relevance: 4,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Hall, R.H. and Hanna, P. The Impact of Web Page Text-Background Color Combinations on Readability, Retention, Aesthetics, and Behavioural Intention.',
          fileName: 'hall_and_hanna_2004.pdf'
        },
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        },
        {
          title: 'Reber, R., Winkielman, P., and Schwarz, N. Effects of Perceptual Fluency on Affective Judgments.',
          fileName: 'reber_et_al_1998.pdf'
        },
        {
          title: 'Reber, R., Wurtz, P., and Zimmermann, T.D. Exploring "fringe" Consciousness: The Subjective Experience of Perceptual Fluency and its Objective Bases.',
          fileName: 'reber_et_al_2004.pdf'
        }
      ],
      results: [
        {
          id: 'pf4_0',
          index: 0,
          type: 'float',
          name: 'Figure-Ground Contrast',
          description: 'Weighted sum of edge pixels divided by sum of edge pixels.',
          scores: [
            {
              id: 'r1',
              range: [null, null],
              description: 'TODO'
            }
          ]
        }
      ]
    },
    pf5: {
      id: 'pf5',
      name: 'Pixel Symmetry',
      category: 'pf',
      description: 'Pixel symmetry indicates perceived symmetricity across an axis. It is associated with the Gestalt principle of symmetry. This metric considers the whole image and finds an axis for maximum symmetry. The metric may be more apt for drawings and photos than user interfaces where elements are unique.',
      evidence: 4,
      relevance: 2,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Quantification of Interface Visual Complexity.',
          fileName: 'miniukovich_and_de_angeli_2014.pdf'
        }
      ],
      results: [
        {
          id: 'pf5_0',
          index: 0,
          type: 'float',
          name: 'Normalized Symmetry',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [0.00, 1.00],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [1.01, null],
              description: 'Poor'
            }
          ]
        }
      ]
    },
    pf6: {
      id: 'pf6',
      name: 'Quadtree decomposition',
      category: 'pf',
      description: 'Quadtree decomposition indicates visual complexity of a scene. It recursively breaks down the image into regions based on entropy in colour and luminance channels.',
      evidence: 3,
      relevance: 3,
      speed: 0,
      visualizationType: 'table',
      references: [
        {
          title: 'Ngo, D.C.L., Teo, L.S., and Byrne, J.G. Modelling Interface Aesthetics.',
          fileName: 'ngo_et_al_2003.pdf'
        },
        {
          title: 'Zheng, X.S., Chakraborty, I., Lin, J.J.-W., and Rauschenberger, R. Correlating Low-Level Image Statistics with Users\' Rapid Aesthetic and Affective Judgments of Web Pages.',
          fileName: 'zheng_et_al_2009.pdf'
        },
        {
          title: 'Reinecke, K., Yeh, T., Miratrix, L., Mardiko, R., Zhao, Y., Liu, J., and Gajos, K.Z. Predicting Users\' First Impressions of Website Aesthetics with a Quantification of Perceived Visual Complexity and Colorfulness.',
          fileName: 'reinecke_et_al_2013.pdf'
        }
      ],
      results: [
        {
          id: 'pf6_0',
          index: 0,
          type: 'float',
          name: 'Balance',
          description: 'Balance can be defined as the distribution of optical weight in a picture. Optical weight refers to the perception that some objects appear heavier than others. Larger objects are heavier, whereas small objects are lighter. Balance in screen design is achieved by providing an equal weight of screen elements, left and right, top and bottom.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.65],
              description: 'Potential unbalanced'
            },
            {
              id: 'r2',
              range: [0.66, 1.00],
              description: 'Balanced'
            }
          ]
        },
        {
          id: 'pf6_1',
          index: 1,
          type: 'float',
          name: 'Symmetry',
          description: 'Symmetry is axial duplication: a unit on one side of the centre line is exactly replicated on the other side. Vertical symmetry refers to the balanced arrangement of equivalent elements about a vertical axis, and horizontal symmetry about a horizontal axis. Radial symmetry consists of equivalent elements balanced about two or more axes that intersect at a central point.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.50],
              description: 'Poor'
            },
            {
              id: 'r2',
              range: [0.51, 1.00],
              description: 'Acceptable'
            }
          ]
        },
        {
          id: 'pf6_2',
          index: 2,
          type: 'float',
          name: 'Equilibrium',
          description: 'Equilibrium is a stabilisation, a midway centre of suspension. Equilibrium on a screen is accomplished through centring the layout itself. The centre of the layout coincides with that of the frame.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.65],
              description: 'Not centralized'
            },
            {
              id: 'r2',
              range: [0.66, 1.00],
              description: 'Centralized'
            }
          ]
        },
        {
          id: 'pf6_3',
          index: 3,
          type: 'int',
          name: 'Number of Leaves',
          description: 'Number of leaves is the total amount of leaves at the end of the recursion. The higher this number, the higher the complexity.',
          scores: [
            {
              id: 'r1',
              range: [0, 1500],
              description: 'Good'
            },
            {
              id: 'r2',
              range: [1501, 3200],
              description: 'Fair'
            },
            {
              id: 'r3',
              range: [3201, null],
              description: 'Poor'
            }
          ]
        }
      ]
    },
    pf7: {
      id: 'pf7',
      name: 'White Space',
      category: 'pf',
      description: 'The proportion of white space indicates, on one hand, effective use of space and, on the other, ability of the interface to guide attention to regions on the user interface. This metric is a heuristic and not based on a theory of human visual system',
      evidence: 2,
      relevance: 4,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'pf7_0',
          index: 0,
          type: 'float',
          name: 'White Space',
          description: 'Proportion of white space.',
          scores: [
            {
              id: 'r1',
              range: [0.00, 0.30],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [0.31, 0.80],
              description: 'Good'
            },
            {
              id: 'r3',
              range: [0.81, 1.00],
              description: 'High'
            }
          ]
        }
      ]
    },
    pf8: {
      id: 'pf8',
      name: 'Grid quality',
      category: 'pf8',
      description: 'Grid quality indicates the internal alignment of the various components or identifiable regions of the UI with respect to each other. Several studies have established that the grid quality has a strong impact on the aesthetic impression induced by the overall layout. Specifically, the measures "G2 and G5" (pp. 1166,Table 3) have been adapted for the evaluation of grid layouts within web pages.',
      evidence: 4,
      relevance: 4,
      speed: 2,
      visualizationType: 'table',
      references: [
        {
          title: 'Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.',
          fileName: 'miniukovich_and_de_angeli_2015.pdf'
        }
      ],
      results: [
        {
          id: 'pf8_0',
          index: 0,
          type: 'int',
          name: 'Number of Alignment Lines',
          description: false,
          scores: [
            {
              id: 'r1',
              range: [4, 100],
              description: 'Low'
            },
            {
              id: 'r2',
              range: [101, 220],
              description: 'Medium'
            },
            {
              id: 'r3',
              range: [221, null],
              description: 'High'
            }
          ]
        }
      ]
    },
    vg1: {
      id: 'vg1',
      name: 'Saliency',
      category: 'vg',
      description: 'Saliency refers to visual conspicuity of regions on the interface. It predicts which areas attract attention when seeing the interface for the first time or when searching for information.',
      evidence: 5,
      relevance: 4,
      speed: 2,
      visualizationType: 'b64',
      references: [
        {
          title: 'Itti, L. and Koch, C. A Saliency-based Search Mechanism for Overt and Covert Shifts of Visual Attention.',
          fileName: 'itti_and_koch_2000.pdf'
        }
      ],
      results: [
        {
          id: 'vg1_0',
          index: 0,
          type: 'b64',
          name: 'Saliency',
          description: 'An overview of the most salient places on the interface.'
        }
      ]
    },
    vg2: {
      id: 'vg2',
      name: 'Visual search performance (experimental)',
      category: 'vg',
      description: 'Visual search performance indicates the ease with which different elements can be found from the image after some experience with the layout. ',
      evidence: 4,
      relevance: 5,
      speed: 0,
      visualizationType: 'b64',
      references: [
        {
          title: 'Jokinen, J.P.P., Sarcar, S, Oulasvirta, A., Silpasuwanchai, C., Wang, Z., and Ren, X. Modelling Learning of New Keyboard Layouts',
          fileName: 'jokinen_et_al_2017.pdf'
        }
      ],
      results: [
        {
          id: 'vg2_0',
          index: 0,
          type: 'b64',
          name: 'Search Speed',
          description: 'Average search time of page elements.'
        }
      ]
    },
    ac1: {
      id: 'ac1',
      name: 'Colour blindness',
      category: 'ac',
      description: 'These metrics indicate information loss for users with color vision deficiencies. The metrics are physiologically motivated and currently handle anomalous trichromacy and dichromacy. Evidence for the metric come from controlled experiments.',
      evidence: 4,
      relevance: 5,
      speed: 1,
      visualizationType: 'b64',
      references: [
        {
          title: 'Machado, G.M., Oliveira, M.M., and Fernandes, L.A.F. A Physiologically-based Model for Simulation of Color Vision Deficiency.',
          fileName: 'machado_et_al_2009.pdf'
        }
      ],
      results: [
        {
          id: 'ac1_0',
          index: 0,
          type: 'b64',
          name: 'Deuteranopia',
          description: 'Red-green color blindness, lacking red cones.'
        },
        {
          id: 'ac1_1',
          index: 1,
          type: 'b64',
          name: 'Protanopia',
          description: 'Red-green color blindness, lacking green cones.'
        },
        {
          id: 'ac1_2',
          index: 2,
          type: 'b64',
          name: 'Tritanopia',
          description: 'Blue-yellow color blindness.'
        }
      ]
    }
  }
}
