/***************************************************************************************************
 * Copyright (c) 2023 - 2024 Marwan Abdellah < abdellah.marwan@gmail.com >
 * Copyright (C) 1994 - Michael Holst and Zeyun Yu
 *
 * This file is part of OMesh, the OptimizationMesh library.
 *
 * This library is free software; you can redistribute it and/or modify it under the terms of the
 * GNU General Public License version 3.0 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU General Public License along with this library;
 * if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
 * MA 02111-1307, USA.
 * You can also find it on the GNU web site < https://www.gnu.org/licenses/gpl-3.0.en.html >
 *
 * OMesh is based on the GAMer (Geometry-preserving Adaptive MeshER) library, which is
 * redistributable and is modifiable under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation as published by the Free Software
 * Foundation; either version 2.1 of the License, or any later version.
 **************************************************************************************************/

#pragma once

#include "Common.hh"

/**
 * @brief The Timer class
 */
class Timer
{
public:

    /**
     * @brief Timer
     */
    Timer() { }

    /**
     * @brief setStart
     */
    void setStart() { _startingTime = std::chrono::high_resolution_clock::now(); }

    /**
     * @brief getTimeMicroSeconds
     * @return
     */
    double getTimeMicroSeconds()
    {
        _endTime = std::chrono::high_resolution_clock::now();
        return std::chrono::duration< double, std::micro >(_endTime-_startingTime).count();
    }

    /**
     * @brief getTimeMilliSeconds
     * @return
     */
    double getTimeMilliSeconds()
    {
        _endTime = std::chrono::high_resolution_clock::now();
        return std::chrono::duration< double, std::milli >(_endTime-_startingTime).count();
    }

    /**
     * @brief getTimeSeonds
     * @return
     */
    double getTimeSeonds()
    {
       _endTime = std::chrono::high_resolution_clock::now();
        return std::chrono::duration< double, std::milli >(_endTime-_startingTime).count() * 1e-3;
    }

private:

    /**
     * @brief _startingTime
     */
    std::chrono::time_point<std::chrono::high_resolution_clock> _startingTime;

    /**
     * @brief _endTime
     */
    std::chrono::time_point<std::chrono::high_resolution_clock> _endTime;
};


// Sets a timer and starts it
#define TIMER_SET Timer timer; timer.setStart()

// Resets a previously declared timer
#define TIMER_RESET timer.setStart()

// Gets the time in seconds, TIMER_SET must be called before calling this
#define GET_TIME_SECONDS timer.getTimeSeonds()

// Gets the time in milli-seconds, TIMER_SET must be called before calling this
#define GET_TIME_MILLI_SECONDS timer.getTimeMilliSeconds()

// Gets the time in micro-seconds, TIMER_SET must be called before calling this
#define GET_TIME_MICRO_SECONDS timer.getTimeMicroSeconds()
